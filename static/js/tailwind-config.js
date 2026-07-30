tailwind.config = {
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        background: "var(--color-background)",
        surface: "var(--color-surface)",
        activeEl: "var(--color-activeEl)",
        cardHover: "var(--color-cardHover)",
        primary: "var(--color-primary)",
        primaryDark: "var(--color-primaryDark)",
        light: "var(--color-light)",
        foreground: "var(--color-foreground)",
        muted: "var(--color-muted)",
        secondary: "var(--color-secondary)",
        border: "var(--color-border)",
        card: "var(--color-card)",
        fade: "var(--color-fade)",
        nav: "var(--color-nav)",
        "nav-border": "var(--color-nav-border)",
      },
      fontFamily: {
        sans: ["Inter", "sans-serif"],
        mono: ["JetBrains Mono", "monospace"],
      },
    },
  },
};
