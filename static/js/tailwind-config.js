window.tailwind = window.tailwind || {};

window.tailwind.config = {
    theme: {
        extend: {
            colors: {
                background: '#030A10',
                surface: '#060F17',
                activeEl: '#081529',

                cardHover: '#0E1823',

                primary: '#2F67D3',
                primaryDark: '#0E2353',
                light: '#8AD0FF',

                foreground: '#FFFEFC',
                muted: '#758293',
            },

            fontFamily: {
                sans: ['Inter', 'sans-serif'],
                mono: ['JetBrains Mono', 'monospace'],
            },
        },
    },
};