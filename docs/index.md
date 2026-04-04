<div class="hero-shell">
  <div class="hero-copy">
    <p class="hero-kicker">Agent orchestration, documented properly</p>
    <h1>Build multi-agent workflows with a docs site that finally feels intentional.</h1>
    <p class="hero-lead">
      Aeon combines <strong>ORCH</strong> for routing, <strong>AEON</strong> for agent behavior, and
      <strong>LIB</strong> for reusable functions. This site gives the language a polished front door:
      clearer structure, cleaner URLs, and a darker visual style that feels much closer to a product docs experience.
    </p>
    <div class="hero-actions">
      <a class="btn btn-primary" href="guide/">Start with the guide</a>
      <a class="btn btn-secondary" href="guide/orch-files/">Read ORCH syntax</a>
    </div>
    <div class="hero-metrics">
      <div class="metric-card">
        <span class="metric-value">3</span>
        <span class="metric-label">core file types</span>
      </div>
      <div class="metric-card">
        <span class="metric-value">1</span>
        <span class="metric-label">routing language</span>
      </div>
      <div class="metric-card">
        <span class="metric-value">Many</span>
        <span class="metric-label">agent workflows</span>
      </div>
    </div>
  </div>
  <div class="hero-visual">
    <img src="assets/aeon-hero.svg" alt="Abstract Aeon orchestration graphic with agents, routing lines, and code panels.">
  </div>
</div>

<div class="spotlight-grid">
  <section class="glass-card">
    <p class="section-kicker">What lives in an Aeon project</p>
    <h2>Three files, one mental model</h2>
    <div class="feature-list">
      <div class="feature-row">
        <span class="feature-pill orch">.orch</span>
        <p>Define the global flow, load agents, and control which path runs next.</p>
      </div>
      <div class="feature-row">
        <span class="feature-pill aeon">.aeon</span>
        <p>Describe a single agent with state, tasks, and local routing.</p>
      </div>
      <div class="feature-row">
        <span class="feature-pill lib">.lib</span>
        <p>Keep reusable Python-backed functions in one shared place.</p>
      </div>
    </div>
  </section>

  <section class="glass-card command-card">
    <p class="section-kicker">Quick look</p>
    <h2>The architecture in one glance</h2>
    <pre class="terminal-window"><code>project/
|-- traffic.orch
|-- agents/
|   |-- intersection.aeon
|   `-- report.aeon
`-- shared/
    `-- math.lib</code></pre>
    <p class="card-note">ORCH wires the system. AEON files hold behavior. LIB files provide reusable logic.</p>
  </section>
</div>

<section class="section-block">
  <p class="section-kicker">Start here</p>
  <h2>Pick the piece you want to understand first</h2>
  <div class="doc-grid">
    <a class="doc-card" href="guide/">
      <span class="doc-card-label">Overview</span>
      <h3>Understand how the DSL fits together</h3>
      <p>Get the big picture before you dive into syntax details.</p>
    </a>
    <a class="doc-card" href="guide/orch-files/">
      <span class="doc-card-label">ORCH</span>
      <h3>Control execution and routing</h3>
      <p>See how includes, globals, conditions, and lifecycle hooks shape a run.</p>
    </a>
    <a class="doc-card" href="guide/aeon-files/">
      <span class="doc-card-label">AEON</span>
      <h3>Define one agent at a time</h3>
      <p>Model state, expose values, write tasks, and create local routes.</p>
    </a>
    <a class="doc-card" href="guide/lib-files/">
      <span class="doc-card-label">LIB</span>
      <h3>Reuse logic across the project</h3>
      <p>Keep helper functions shared and keep your agents focused.</p>
    </a>
  </div>
</section>

<section class="section-block">
  <p class="section-kicker">Why this layout works better</p>
  <h2>Made to feel closer to GitBook, not a starter template</h2>
  <div class="journey-grid">
    <div class="journey-card">
      <h3>Clean nav</h3>
      <p>Guide pages live under readable paths like <code>/guide/orch-files/</code> instead of hashed filenames.</p>
    </div>
    <div class="journey-card">
      <h3>Focused reading</h3>
      <p>A docs sidebar, page summary, and right-side table of contents keep long pages easy to scan.</p>
    </div>
    <div class="journey-card">
      <h3>Dark visual identity</h3>
      <p>Gradients, glass panels, and a custom hero graphic give the site a stronger product feel.</p>
    </div>
  </div>
</section>
