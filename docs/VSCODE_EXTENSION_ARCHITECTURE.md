# AutoPR VS Code Extension Architecture

## Overview

AutoPR VS Code Extension brings AI-powered PR description generation and code review directly into the editor, supporting both local (offline) and hosted API modes.

---

## Features

1. **Generate PR Description from Git Diff** - Analyze staged/committed changes and generate comprehensive PR descriptions
2. **Manual AI Review Comments** - User-triggered code review with confidence-scored feedback
3. **One-Click Copy to GitHub PR** - Copy generated content or open GitHub PR creation page
4. **Dual Mode Operation** - Works locally without server OR via hosted API

---

## Hardening Features for Real-World Usage

### 1. Confidence-Scored AI Review Comments

**UX Decision**: Display confidence levels (High/Medium/Low) with review comments to help users gauge reliability. Low-confidence comments are shown but visually de-emphasized. Users can filter by confidence threshold in settings.

**Implementation**: LLM providers return confidence scores (0-1) with each review comment. Comments below threshold are styled with reduced opacity and optional filtering.

```typescript
interface ReviewComment {
  line: number;
  message: string;
  severity: 'info' | 'warning' | 'error';
  confidence: number; // 0-1 scale
  suggestion?: string;
}

class ReviewRenderer {
  private confidenceThreshold: number = 0.6;

  renderComment(comment: ReviewComment): vscode.DecorationOptions | null {
    if (comment.confidence < this.confidenceThreshold) {
      return null; // Filter out low-confidence comments
    }

    const opacity = Math.max(0.3, comment.confidence);
    return {
      range: new vscode.Range(comment.line, 0, comment.line, 0),
      renderOptions: {
        after: {
          contentText: `💬 ${comment.message}`,
          color: `rgba(255, 255, 255, ${opacity})`,
          backgroundColor: this.getSeverityColor(comment.severity, opacity)
        }
      }
    };
  }
}
```

### 2. Manual-Triggered Review (No Auto-Spam)

**UX Decision**: Reviews only trigger on explicit user command to prevent overwhelming the editor. Status bar shows "Review Available" indicator when changes are detected, but doesn't auto-analyze.

**Implementation**: Remove automatic CodeLens on file open. Add status bar item that lights up when diff changes are detected.

```typescript
class ReviewStatusBar {
  private item: vscode.StatusBarItem;
  private hasUnreviewedChanges: boolean = false;

  constructor() {
    this.item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 100);
    this.item.command = 'autopr.reviewChanges';
    this.update();
  }

  update() {
    if (this.hasUnreviewedChanges) {
      this.item.text = '$(eye) Review Available';
      this.item.tooltip = 'Click to review current changes';
      this.item.show();
    } else {
      this.item.hide();
    }
  }

  markChangesAvailable() {
    this.hasUnreviewedChanges = true;
    this.update();
  }

  markReviewed() {
    this.hasUnreviewedChanges = false;
    this.update();
  }
}
```

### 3. Diff-Based Caching with Hash Keys

**UX Decision**: Cache review results to avoid redundant API calls. Cache invalidates when diff changes. Users see "cached" indicator for instant results.

**Implementation**: Generate SHA-256 hash of diff content as cache key. Store results in workspace storage with TTL.

```typescript
import { createHash } from 'crypto';

class ReviewCache {
  private cache: Map<string, CachedReview> = new Map();
  private readonly TTL = 30 * 60 * 1000; // 30 minutes

  getCacheKey(diff: string): string {
    return createHash('sha256').update(diff).digest('hex');
  }

  async get(key: string): Promise<ReviewComment[] | null> {
    const cached = this.cache.get(key);
    if (!cached) return null;

    if (Date.now() - cached.timestamp > this.TTL) {
      this.cache.delete(key);
      return null;
    }

    return cached.comments;
  }

  set(key: string, comments: ReviewComment[]): void {
    this.cache.set(key, {
      comments,
      timestamp: Date.now()
    });
  }

  invalidate(): void {
    this.cache.clear();
  }
}

interface CachedReview {
  comments: ReviewComment[];
  timestamp: number;
}
```

### 4. Editable PR Preview with State Sync

**UX Decision**: PR preview is fully editable with real-time sync between webview and extension. Changes persist across sessions. Clear save/discard options prevent accidental loss.

**Implementation**: Webview uses contentEditable with message passing for state sync. Extension stores draft in workspace storage.

```typescript
class PRPreviewPanel {
  private panel: vscode.WebviewPanel;
  private currentContent: string = '';
  private isDirty: boolean = false;

  constructor(extensionUri: vscode.Uri) {
    this.panel = vscode.window.createWebviewPanel(
      'autopr.preview',
      'PR Preview',
      vscode.ViewColumn.One,
      { enableScripts: true }
    );

    this.panel.webview.html = this.getHtml();
    this.setupMessageHandling();
    this.loadDraft();
  }

  private setupMessageHandling() {
    this.panel.webview.onDidReceiveMessage(async (message) => {
      switch (message.type) {
        case 'contentChanged':
          this.currentContent = message.content;
          this.isDirty = true;
          await this.saveDraft();
          break;
        case 'save':
          await this.persistContent();
          this.isDirty = false;
          break;
        case 'discard':
          await this.loadDraft();
          this.isDirty = false;
          break;
      }
    });
  }

  private async saveDraft(): Promise<void> {
    const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
    if (workspaceFolder) {
      await vscode.workspace.getConfiguration('autopr').update(
        'prDraft',
        this.currentContent,
        vscode.ConfigurationTarget.Workspace
      );
    }
  }

  private async loadDraft(): Promise<void> {
    const draft = vscode.workspace.getConfiguration('autopr').get('prDraft', '');
    this.currentContent = draft;
    this.panel.webview.postMessage({
      type: 'loadContent',
      content: draft
    });
  }
}
```

### 5. Clear User-Facing Privacy Messaging

**UX Decision**: Prominent privacy notices in setup flow and status messages. Different messaging for local vs hosted modes. Users can see exactly what data is sent where.

**Implementation**: Privacy panel on first use, status bar privacy indicator, and detailed tooltips.

```typescript
class PrivacyManager {
  async showPrivacyNotice(): Promise<boolean> {
    const mode = vscode.workspace.getConfiguration('autopr').get('mode', 'local');

    const message = mode === 'local'
      ? 'AutoPR runs locally. Code stays on your machine.'
      : 'AutoPR uses hosted API. Code diffs will be sent to external service.';

    const result = await vscode.window.showInformationMessage(
      message,
      { modal: true },
      'Continue',
      'Configure Privacy'
    );

    if (result === 'Configure Privacy') {
      await this.openPrivacySettings();
      return false;
    }

    return result === 'Continue';
  }

  private async openPrivacySettings(): Promise<void> {
    const panel = vscode.window.createWebviewPanel(
      'autopr.privacy',
      'AutoPR Privacy Settings',
      vscode.ViewColumn.One,
      { enableScripts: true }
    );

    panel.webview.html = this.getPrivacyHtml();
  }

  private getPrivacyHtml(): string {
    const mode = vscode.workspace.getConfiguration('autopr').get('mode', 'local');

    return `
      <h2>AutoPR Privacy Settings</h2>
      <div class="privacy-section">
        <h3>Data Handling</h3>
        <p><strong>Local Mode:</strong> All processing happens on your machine. No data leaves your device.</p>
        <p><strong>Hosted Mode:</strong> Code diffs and commit messages are sent to ${this.getEndpoint()}. API keys are stored securely.</p>
        <p><strong>OpenAI Mode:</strong> Data sent to OpenAI's API. Review OpenAI's privacy policy.</p>
      </div>
      <div class="privacy-section">
        <h3>What We Collect</h3>
        <ul>
          <li>Git diff content (filtered for sensitive files)</li>
          <li>Commit messages</li>
          <li>Repository metadata (name, branch)</li>
        </ul>
      </div>
    `;
  }
}
```

---

## Extension Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      VS Code Extension Host                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │   Commands   │  │   TreeView   │  │   CodeLens Provider  │  │
│  │   Handler    │  │   Provider   │  │   (Inline Reviews)   │  │
│  └──────┬───────┘  └──────┬───────┘  └──────────┬───────────┘  │
│         │                 │                      │               │
│         └─────────────────┼──────────────────────┘               │
│                           │                                      │
│                    ┌──────▼───────┐                             │
│                    │  AutoPR Core │                             │
│                    │   Service    │                             │
│                    └──────┬───────┘                             │
│                           │                                      │
│         ┌─────────────────┼─────────────────┐                   │
│         │                 │                 │                    │
│  ┌──────▼───────┐  ┌──────▼───────┐  ┌─────▼──────┐            │
│  │  Git Service │  │  LLM Service │  │  GitHub    │            │
│  │  (simple-git)│  │              │  │  Service   │            │
│  └──────────────┘  └──────┬───────┘  └────────────┘            │
│                           │                                      │
│              ┌────────────┼────────────┐                        │
│              │            │            │                         │
│       ┌──────▼────┐ ┌─────▼─────┐ ┌───▼────┐                   │
│       │  Local    │ │  Hosted   │ │ OpenAI │                   │
│       │  Ollama   │ │  AutoPR   │ │  API   │                   │
│       │           │ │  API      │ │        │                   │
│       └───────────┘ └───────────┘ └────────┘                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Folder Structure

```
autopr-vscode/
├── .vscode/
│   ├── launch.json              # Debug configurations
│   └── tasks.json               # Build tasks
├── src/
│   ├── extension.ts             # Extension entry point
│   ├── commands/
│   │   ├── index.ts             # Command registration
│   │   ├── generatePR.ts        # Generate PR description command
│   │   ├── reviewCode.ts        # Review code command
│   │   └── copyToGitHub.ts      # Copy/open GitHub PR
│   ├── services/
│   │   ├── gitService.ts        # Git operations (diff, commits, branch)
│   │   ├── llmService.ts        # LLM abstraction layer
│   │   ├── githubService.ts     # GitHub API interactions
│   │   └── autoprCore.ts        # Core AutoPR logic
│   ├── providers/
│   │   ├── localProvider.ts     # Ollama/local LLM provider
│   │   ├── hostedProvider.ts    # Hosted AutoPR API provider
│   │   └── openaiProvider.ts    # Direct OpenAI provider
│   ├── views/
│   │   ├── prPreviewPanel.ts    # Webview for PR preview
│   │   ├── reviewTreeView.ts    # Tree view for review comments
│   │   └── codeLensProvider.ts  # Inline review decorations
│   ├── utils/
│   │   ├── config.ts            # Configuration management
│   │   ├── secrets.ts           # Secure credential storage
│   │   └── diff.ts              # Diff parsing utilities
│   └── types/
│       ├── index.ts             # Type definitions
│       ├── review.ts            # Review-related types
│       └── pr.ts                # PR-related types
├── webview/
│   ├── prPreview/
│   │   ├── index.html           # PR preview HTML
│   │   ├── main.ts              # Preview logic
│   │   └── styles.css           # Preview styles
│   └── reviewPanel/
│       ├── index.html           # Review panel HTML
│       └── main.ts              # Review panel logic
├── test/
│   ├── suite/
│   │   ├── extension.test.ts
│   │   ├── gitService.test.ts
│   │   └── llmService.test.ts
│   └── runTest.ts
├── package.json                  # Extension manifest
├── tsconfig.json                 # TypeScript config
├── webpack.config.js             # Build configuration
├── CHANGELOG.md
├── README.md
└── LICENSE
```

---

## Message Flow

### 1. Generate PR Description Flow

```
┌────────┐     ┌─────────────┐     ┌───────────┐     ┌───────────┐
│  User  │────▶│  VS Code    │────▶│  AutoPR   │────▶│  Git      │
│        │     │  Command    │     │  Core     │     │  Service  │
└────────┘     └─────────────┘     └─────┬─────┘     └─────┬─────┘
                                         │                 │
                                         │  1. Get diff    │
                                         │◀────────────────┤
                                         │                 │
                                   ┌─────▼─────┐          │
                                   │  LLM      │          │
                                   │  Service  │          │
                                   └─────┬─────┘          │
                                         │                 │
                    ┌────────────────────┼────────────────┐
                    │                    │                │
             ┌──────▼──────┐      ┌──────▼──────┐  ┌─────▼─────┐
             │   Local     │      │   Hosted    │  │  OpenAI   │
             │   Ollama    │      │   API       │  │   API     │
             └──────┬──────┘      └──────┬──────┘  └─────┬─────┘
                    │                    │                │
                    └────────────────────┼────────────────┘
                                         │
                                   ┌─────▼─────┐
                                   │  PR       │
                                   │  Preview  │
                                   │  Webview  │
                                   └───────────┘
```

### 2. Inline Review Comments Flow

```
┌──────────────┐     ┌──────────────┐     ┌───────────────┐
│  Manual      │────▶│  CodeLens    │────▶│  AutoPR       │
│  Command     │     │  Provider    │     │  Review       │
└──────────────┘     └──────────────┘     └───────┬───────┘
                                                │
                          ┌─────────────────────┼─────────────────────┐
                          │                     │                     │
                   ┌──────▼──────┐       ┌──────▼──────┐       ┌─────▼─────┐
                   │  Cached     │       │  LLM        │       │  Parse    │
                   │  Results    │       │  Analysis   │       │  Diff     │
                   └──────┬──────┘       └──────┬──────┘       └───────────┘
                          │                     │
                          └──────────┬──────────┘
                                     │
                              ┌──────▼──────┐
                              │  Inline     │
                              │  Decoration │
                              └─────────────┘
```

### 3. Copy to GitHub PR Flow

```
┌────────┐     ┌─────────────┐     ┌───────────────┐     ┌───────────┐
│  User  │────▶│  Copy/Open  │────▶│  GitHub       │────▶│  GitHub   │
│        │     │  Command    │     │  Service      │     │  API/Web  │
└────────┘     └─────────────┘     └───────┬───────┘     └───────────┘
                                           │
                     ┌─────────────────────┼─────────────────────┐
                     │                     │                     │
              ┌──────▼──────┐       ┌──────▼──────┐       ┌─────▼─────┐
              │  Copy to    │       │  Open PR    │       │  Create   │
              │  Clipboard  │       │  Creation   │       │  PR via   │
              │             │       │  Page       │       │  API      │
              └─────────────┘       └─────────────┘       └───────────┘
```

---

## Security Considerations

### 1. Credential Storage

```typescript
// Use VS Code's SecretStorage API for sensitive data
class SecretsManager {
  constructor(private context: vscode.ExtensionContext) {}

  async storeApiKey(provider: string, key: string): Promise<void> {
    await this.context.secrets.store(`autopr.${provider}.apiKey`, key);
  }

  async getApiKey(provider: string): Promise<string | undefined> {
    return this.context.secrets.get(`autopr.${provider}.apiKey`);
  }

  async deleteApiKey(provider: string): Promise<void> {
    await this.context.secrets.delete(`autopr.${provider}.apiKey`);
  }
}
```

### 2. Security Best Practices

| Concern | Mitigation |
|---------|------------|
| **API Key Exposure** | Store in VS Code SecretStorage, never in settings.json |
| **Code Transmission** | Use HTTPS for all API calls; local mode keeps data on device |
| **GitHub Token Scope** | Request minimum scopes: `repo`, `read:user` |
| **Local LLM Privacy** | Ollama runs entirely locally, no data leaves machine |
| **Sensitive Data in Diffs** | Option to exclude files matching patterns (`.env`, `*.key`) |
| **Webview Security** | Use Content Security Policy, sanitize all HTML |

### 3. Content Security Policy for Webviews

```typescript
function getWebviewOptions(): vscode.WebviewOptions {
  return {
    enableScripts: true,
    localResourceRoots: [extensionUri],
  };
}

function getContentSecurityPolicy(webview: vscode.Webview, nonce: string): string {
  return `
    default-src 'none';
    style-src ${webview.cspSource} 'unsafe-inline';
    script-src 'nonce-${nonce}';
    img-src ${webview.cspSource} https: data:;
  `;
}
```

### 4. Sensitive File Filtering

```typescript
// Default patterns to exclude from analysis
const SENSITIVE_PATTERNS = [
  '**/.env*',
  '**/*.key',
  '**/*.pem',
  '**/*.p12',
  '**/credentials*',
  '**/secrets*',
  '**/*password*',
  '**/id_rsa*',
];
```

---

## Configuration Schema

```json
{
  "autopr.mode": {
    "type": "string",
    "enum": ["local", "hosted", "openai"],
    "default": "local",
    "description": "LLM provider mode"
  },
  "autopr.local.endpoint": {
    "type": "string",
    "default": "http://localhost:11434",
    "description": "Ollama API endpoint"
  },
  "autopr.local.model": {
    "type": "string",
    "default": "codellama",
    "description": "Local model to use"
  },
  "autopr.hosted.endpoint": {
    "type": "string",
    "default": "https://api.autopr.dev",
    "description": "Hosted AutoPR API endpoint"
  },
  "autopr.github.autoOpen": {
    "type": "boolean",
    "default": true,
    "description": "Auto-open GitHub PR creation page"
  },
  "autopr.review.enabled": {
    "type": "boolean",
    "default": true,
    "description": "Enable inline review comments"
  },
  "autopr.excludePatterns": {
    "type": "array",
    "default": ["**/.env*", "**/*.key"],
    "description": "File patterns to exclude from analysis"
  },
  "autopr.review.confidenceThreshold": {
    "type": "number",
    "default": 0.6,
    "minimum": 0,
    "maximum": 1,
    "description": "Minimum confidence score for review comments (0-1)"
  },
  "autopr.review.enableCaching": {
    "type": "boolean",
    "default": true,
    "description": "Cache review results to avoid redundant API calls"
  },
  "autopr.privacy.showNotices": {
    "type": "boolean",
    "default": true,
    "description": "Show privacy notices and data handling information"
  }
}
```

---

## package.json Contribution Points

```json
{
  "name": "autopr-vscode",
  "displayName": "AutoPR",
  "version": "1.0.0",
  "engines": { "vscode": "^1.85.0" },
  "categories": ["Other", "SCM Providers"],
  "activationEvents": [
    "onStartupFinished",
    "workspaceContains:.git"
  ],
  "main": "./dist/extension.js",
  "contributes": {
    "commands": [
      {
        "command": "autopr.generatePR",
        "title": "Generate PR Description",
        "category": "AutoPR",
        "icon": "$(git-pull-request)"
      },
      {
        "command": "autopr.reviewFile",
        "title": "Review Current File",
        "category": "AutoPR"
      },
      {
        "command": "autopr.reviewChanges",
        "title": "Review All Changes",
        "category": "AutoPR"
      },
      {
        "command": "autopr.copyToClipboard",
        "title": "Copy PR Description",
        "category": "AutoPR"
      },
      {
        "command": "autopr.openGitHubPR",
        "title": "Open GitHub PR Creation",
        "category": "AutoPR"
      },
      {
        "command": "autopr.configure",
        "title": "Configure AutoPR",
        "category": "AutoPR"
      }
    ],
    "menus": {
      "scm/title": [
        {
          "command": "autopr.generatePR",
          "group": "navigation",
          "when": "scmProvider == git"
        }
      ],
      "editor/title": [
        {
          "command": "autopr.reviewFile",
          "group": "navigation",
          "when": "gitOpenRepositoryCount > 0"
        }
      ]
    },
    "views": {
      "scm": [
        {
          "id": "autoprReview",
          "name": "AutoPR Review",
          "when": "gitOpenRepositoryCount > 0"
        }
      ]
    },
    "configuration": {
      "title": "AutoPR",
      "properties": {
        "autopr.mode": { "...": "..." },
        "autopr.local.endpoint": { "...": "..." }
      }
    }
  }
}
```

---

## Key Implementation Details

### Git Service

```typescript
import simpleGit, { SimpleGit } from 'simple-git';

export class GitService {
  private git: SimpleGit;

  constructor(workspacePath: string) {
    this.git = simpleGit(workspacePath);
  }

  async getDiff(staged: boolean = true): Promise<string> {
    return staged 
      ? await this.git.diff(['--cached'])
      : await this.git.diff();
  }

  async getCommitMessages(count: number = 10): Promise<string[]> {
    const log = await this.git.log({ maxCount: count });
    return log.all.map(c => c.message);
  }

  async getCurrentBranch(): Promise<string> {
    const branch = await this.git.branch();
    return branch.current;
  }

  async getRemoteUrl(): Promise<string | undefined> {
    const remotes = await this.git.getRemotes(true);
    const origin = remotes.find(r => r.name === 'origin');
    return origin?.refs.fetch;
  }
}
```

### LLM Service Abstraction

```typescript
export interface LLMProvider {
  generatePRDescription(diff: string, commits: string[]): Promise<string>;
  reviewCode(diff: string): Promise<ReviewComment[]>;
}

export class LLMService {
  private provider: LLMProvider;

  constructor(config: AutoPRConfig) {
    switch (config.mode) {
      case 'local':
        this.provider = new LocalProvider(config.local);
        break;
      case 'hosted':
        this.provider = new HostedProvider(config.hosted);
        break;
      case 'openai':
        this.provider = new OpenAIProvider(config.openai);
        break;
    }
  }

  async generatePR(diff: string, commits: string[]): Promise<string> {
    try {
      return await this.provider.generatePRDescription(diff, commits);
    } catch (error) {
      console.error('PR generation failed:', error);
      vscode.window.showErrorMessage('PR description generation failed. Check your configuration.');
      return 'Unable to generate PR description. Please check your LLM configuration.';
    }
  }

  async review(diff: string): Promise<ReviewComment[]> {
    try {
      return await this.provider.reviewCode(diff);
    } catch (error) {
      console.error('Review failed:', error);
      vscode.window.showErrorMessage('AI review failed. Check your configuration and try again.');
      return [];
    }
  }
}
```

---

## Dependencies

```json
{
  "dependencies": {
    "simple-git": "^3.22.0",
    "axios": "^1.6.0",
    "marked": "^11.0.0"
  },
  "devDependencies": {
    "@types/vscode": "^1.85.0",
    "@types/node": "^20.10.0",
    "typescript": "^5.3.0",
    "webpack": "^5.89.0",
    "webpack-cli": "^5.1.0",
    "ts-loader": "^9.5.0",
    "@vscode/test-electron": "^2.3.0"
  }
}
```

---

## Testing Strategy

1. **Unit Tests** - Service layer logic (GitService, LLMService)
2. **Integration Tests** - End-to-end command execution
3. **Mock Providers** - Test LLM integration without API calls
4. **Webview Tests** - Test webview message handling

---

## Future Enhancements

- [ ] Support for GitLab and Bitbucket
- [ ] PR template customization
- [ ] Team-shared review rules
- [ ] Historical PR learning
- [ ] CI/CD integration for automated reviews
