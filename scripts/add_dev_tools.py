"""Add comprehensive testing, DevOps, IDE, build, debugging, and code quality tools."""
import json

with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

existing = {i.get('name', '').lower() for i in data}

new_items = [
    # Testing - more comprehensive
    {'name': 'Mocha', 'url': 'https://mochajs.org/', 'category': 'Testing', 'description': 'Feature-rich JavaScript test framework for Node.js and browsers'},
    {'name': 'Jasmine', 'url': 'https://jasmine.github.io/', 'category': 'Testing', 'description': 'Behavior-driven development testing framework for JavaScript'},
    {'name': 'Puppeteer', 'url': 'https://pptr.dev/', 'category': 'Testing', 'description': 'Headless Chrome Node.js API for browser automation and testing'},
    {'name': 'TestCafe', 'url': 'https://testcafe.io/', 'category': 'Testing', 'description': 'End-to-end testing framework that works on all browsers'},
    {'name': 'WebdriverIO', 'url': 'https://webdriver.io/', 'category': 'Testing', 'description': 'Next-gen browser and mobile automation test framework'},
    {'name': 'Appium', 'url': 'https://appium.io/', 'category': 'Testing', 'description': 'Cross-platform mobile app automation framework'},
    {'name': 'Robot Framework', 'url': 'https://robotframework.org/', 'category': 'Testing', 'description': 'Generic open source automation framework for acceptance testing'},
    {'name': 'Detox', 'url': 'https://wix.github.io/Detox/', 'category': 'Testing', 'description': 'Gray box end-to-end testing for React Native apps'},
    {'name': 'Nightwatch.js', 'url': 'https://nightwatchjs.org/', 'category': 'Testing', 'description': 'End-to-end testing solution for web applications'},
    {'name': 'Codecept', 'url': 'https://codecept.io/', 'category': 'Testing', 'description': 'Modern end-to-end testing framework with special powers'},
    {'name': 'AVA', 'url': 'https://github.com/avajs/ava', 'category': 'Testing', 'description': 'Node.js test runner with concurrent test execution'},
    {'name': 'Tape', 'url': 'https://github.com/ljharb/tape', 'category': 'Testing', 'description': 'Minimal TAP-producing test harness for Node.js'},
    {'name': 'QUnit', 'url': 'https://qunitjs.com/', 'category': 'Testing', 'description': 'JavaScript unit testing framework used by jQuery'},
    {'name': 'Karma', 'url': 'https://karma-runner.github.io/', 'category': 'Testing', 'description': 'Test runner for JavaScript that works with any framework'},
    {'name': 'Storybook', 'url': 'https://storybook.js.org/', 'category': 'Testing', 'description': 'UI component development and testing environment'},
    {'name': 'Chromatic', 'url': 'https://www.chromatic.com/', 'category': 'Testing', 'description': 'Visual testing and review for Storybook components'},
    {'name': 'Percy', 'url': 'https://percy.io/', 'category': 'Testing', 'description': 'Visual testing and review platform for web apps'},
    {'name': 'BrowserStack', 'url': 'https://www.browserstack.com/', 'category': 'Testing', 'description': 'Cross-browser testing platform with real devices'},
    {'name': 'Sauce Labs', 'url': 'https://saucelabs.com/', 'category': 'Testing', 'description': 'Continuous testing cloud for web and mobile apps'},
    {'name': 'LambdaTest', 'url': 'https://www.lambdatest.com/', 'category': 'Testing', 'description': 'Cross browser testing cloud with real browsers'},
    
    # DevOps - more CI/CD tools
    {'name': 'Travis CI', 'url': 'https://www.travis-ci.com/', 'category': 'DevOps', 'description': 'Hosted continuous integration service for open source'},
    {'name': 'Drone', 'url': 'https://www.drone.io/', 'category': 'DevOps', 'description': 'Container-native continuous delivery platform'},
    {'name': 'Spinnaker', 'url': 'https://spinnaker.io/', 'category': 'DevOps', 'description': 'Multi-cloud continuous delivery platform by Netflix'},
    {'name': 'Harness', 'url': 'https://harness.io/', 'category': 'DevOps', 'description': 'Modern software delivery platform with CI/CD'},
    {'name': 'Concourse', 'url': 'https://concourse-ci.org/', 'category': 'DevOps', 'description': 'Pipeline-based continuous integration system'},
    {'name': 'Buildkite', 'url': 'https://buildkite.com/', 'category': 'DevOps', 'description': 'Platform for running fast and secure CI pipelines'},
    {'name': 'TeamCity', 'url': 'https://www.jetbrains.com/teamcity/', 'category': 'DevOps', 'description': 'Powerful CI/CD server by JetBrains'},
    {'name': 'Bamboo', 'url': 'https://www.atlassian.com/software/bamboo', 'category': 'DevOps', 'description': 'CI/CD server by Atlassian for build and deployment'},
    {'name': 'Octopus Deploy', 'url': 'https://octopus.com/', 'category': 'DevOps', 'description': 'Deployment automation for .NET and beyond'},
    {'name': 'Flux', 'url': 'https://fluxcd.io/', 'category': 'DevOps', 'description': 'GitOps toolkit for Kubernetes continuous delivery'},
    {'name': 'Tekton', 'url': 'https://tekton.dev/', 'category': 'DevOps', 'description': 'Cloud-native CI/CD building blocks for Kubernetes'},
    {'name': 'Waypoint', 'url': 'https://www.waypointproject.io/', 'category': 'DevOps', 'description': 'Build, deploy, and release applications by HashiCorp'},
    
    # IDE/Editor - more options  
    {'name': 'Vim', 'url': 'https://www.vim.org/', 'category': 'IDE/Editor', 'description': 'Highly configurable text editor built for efficiency'},
    {'name': 'Emacs', 'url': 'https://www.gnu.org/software/emacs/', 'category': 'IDE/Editor', 'description': 'Extensible, customizable text editor and computing environment'},
    {'name': 'WebStorm', 'url': 'https://www.jetbrains.com/webstorm/', 'category': 'IDE/Editor', 'description': 'Professional IDE for JavaScript by JetBrains'},
    {'name': 'Fleet', 'url': 'https://www.jetbrains.com/fleet/', 'category': 'IDE/Editor', 'description': 'Next-generation IDE by JetBrains'},
    {'name': 'Nova', 'url': 'https://nova.app/', 'category': 'IDE/Editor', 'description': 'Beautiful, fast, flexible native Mac code editor'},
    {'name': 'Lapce', 'url': 'https://lapce.dev/', 'category': 'IDE/Editor', 'description': 'Lightning-fast open source code editor written in Rust'},
    {'name': 'Helix', 'url': 'https://helix-editor.com/', 'category': 'IDE/Editor', 'description': 'Post-modern modal text editor with built-in LSP'},
    {'name': 'CodeSandbox', 'url': 'https://codesandbox.io/', 'category': 'IDE/Editor', 'description': 'Online IDE for rapid web development'},
    {'name': 'StackBlitz', 'url': 'https://stackblitz.com/', 'category': 'IDE/Editor', 'description': 'Instant full-stack web IDE in the browser'},
    {'name': 'Replit', 'url': 'https://replit.com/', 'category': 'IDE/Editor', 'description': 'Collaborative browser-based IDE for 50+ languages'},
    {'name': 'Codespaces', 'url': 'https://github.com/features/codespaces', 'category': 'IDE/Editor', 'description': 'Cloud development environments by GitHub'},
    {'name': 'Gitpod', 'url': 'https://www.gitpod.io/', 'category': 'IDE/Editor', 'description': 'Ready-to-code cloud development environments'},
    
    # Build Tools - more
    {'name': 'Gradle', 'url': 'https://gradle.org/', 'category': 'Build Tool', 'description': 'Build automation tool for multi-language software development'},
    {'name': 'Ant', 'url': 'https://ant.apache.org/', 'category': 'Build Tool', 'description': 'Java library and command-line tool for build processes'},
    {'name': 'Meson', 'url': 'https://mesonbuild.com/', 'category': 'Build Tool', 'description': 'Fast and user-friendly build system'},
    {'name': 'Ninja', 'url': 'https://ninja-build.org/', 'category': 'Build Tool', 'description': 'Small build system with focus on speed'},
    {'name': 'Snowpack', 'url': 'https://www.snowpack.dev/', 'category': 'Build Tool', 'description': 'Lightning-fast frontend build tool for ESM'},
    {'name': 'tsup', 'url': 'https://tsup.egoist.dev/', 'category': 'Build Tool', 'description': 'Bundle TypeScript libraries with zero config'},
    {'name': 'unbuild', 'url': 'https://github.com/unjs/unbuild', 'category': 'Build Tool', 'description': 'Unified JavaScript build system'},
    {'name': 'Bun', 'url': 'https://bun.sh/', 'category': 'Build Tool', 'description': 'All-in-one JavaScript runtime and toolkit'},
    
    # Debugging/Profiling - NEW category
    {'name': 'Chrome DevTools', 'url': 'https://developer.chrome.com/docs/devtools/', 'category': 'Debugging', 'description': 'Web developer tools built into Chrome browser'},
    {'name': 'Firefox DevTools', 'url': 'https://firefox-source-docs.mozilla.org/devtools-user/', 'category': 'Debugging', 'description': 'Web development tools built into Firefox'},
    {'name': 'Lighthouse', 'url': 'https://developer.chrome.com/docs/lighthouse/', 'category': 'Debugging', 'description': 'Automated tool for improving web page quality'},
    {'name': 'React DevTools', 'url': 'https://react.dev/learn/react-developer-tools', 'category': 'Debugging', 'description': 'Browser extension for debugging React applications'},
    {'name': 'Vue DevTools', 'url': 'https://devtools.vuejs.org/', 'category': 'Debugging', 'description': 'Browser devtools extension for Vue.js'},
    {'name': 'Redux DevTools', 'url': 'https://github.com/reduxjs/redux-devtools', 'category': 'Debugging', 'description': 'DevTools for Redux with time-travel debugging'},
    {'name': 'Flipper', 'url': 'https://fbflipper.com/', 'category': 'Debugging', 'description': 'Desktop debugging platform for mobile apps'},
    {'name': 'Reactotron', 'url': 'https://github.com/infinitered/reactotron', 'category': 'Debugging', 'description': 'Desktop app for inspecting React and React Native apps'},
    {'name': 'Sentry', 'url': 'https://sentry.io/', 'category': 'Debugging', 'description': 'Error tracking and performance monitoring'},
    {'name': 'LogRocket', 'url': 'https://logrocket.com/', 'category': 'Debugging', 'description': 'Session replay and error tracking for web apps'},
    {'name': 'Raygun', 'url': 'https://raygun.com/', 'category': 'Debugging', 'description': 'Error monitoring and crash reporting'},
    
    # Code Quality/Linting - NEW category
    {'name': 'ESLint', 'url': 'https://eslint.org/', 'category': 'Code Quality', 'description': 'Pluggable linting utility for JavaScript and JSX'},
    {'name': 'Prettier', 'url': 'https://prettier.io/', 'category': 'Code Quality', 'description': 'Opinionated code formatter for consistent style'},
    {'name': 'Stylelint', 'url': 'https://stylelint.io/', 'category': 'Code Quality', 'description': 'Mighty CSS linter that helps avoid errors'},
    {'name': 'SonarQube', 'url': 'https://www.sonarqube.org/', 'category': 'Code Quality', 'description': 'Continuous code quality and security inspection'},
    {'name': 'CodeClimate', 'url': 'https://codeclimate.com/', 'category': 'Code Quality', 'description': 'Automated code review for maintainability'},
    {'name': 'Codacy', 'url': 'https://www.codacy.com/', 'category': 'Code Quality', 'description': 'Automated code reviews and analytics'},
    {'name': 'Snyk', 'url': 'https://snyk.io/', 'category': 'Code Quality', 'description': 'Developer security platform for code and dependencies'},
    {'name': 'Dependabot', 'url': 'https://github.com/dependabot', 'category': 'Code Quality', 'description': 'Automated dependency updates by GitHub'},
    {'name': 'Renovate', 'url': 'https://www.mend.io/renovate/', 'category': 'Code Quality', 'description': 'Automated dependency updates for any platform'},
    {'name': 'Husky', 'url': 'https://typicode.github.io/husky/', 'category': 'Code Quality', 'description': 'Git hooks made easy for better commits'},
    {'name': 'lint-staged', 'url': 'https://github.com/lint-staged/lint-staged', 'category': 'Code Quality', 'description': 'Run linters on staged git files'},
    {'name': 'commitlint', 'url': 'https://commitlint.js.org/', 'category': 'Code Quality', 'description': 'Lint commit messages for consistency'},
    {'name': 'Ruff', 'url': 'https://docs.astral.sh/ruff/', 'category': 'Code Quality', 'description': 'Extremely fast Python linter written in Rust'},
    {'name': 'Black', 'url': 'https://black.readthedocs.io/', 'category': 'Code Quality', 'description': 'Uncompromising Python code formatter'},
    {'name': 'Pylint', 'url': 'https://pylint.org/', 'category': 'Code Quality', 'description': 'Static code analyzer for Python'},
    {'name': 'RuboCop', 'url': 'https://rubocop.org/', 'category': 'Code Quality', 'description': 'Ruby static code analyzer and formatter'},
    {'name': 'Clippy', 'url': 'https://github.com/rust-lang/rust-clippy', 'category': 'Code Quality', 'description': 'Collection of lints to catch common mistakes in Rust'},
]

added = 0
for item in new_items:
    if item['name'].lower() not in existing:
        data.append(item)
        added += 1
        print(f"Added: {item['name']}")

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f'\nTotal added: {added}')
print(f'New total: {len(data)} items')
