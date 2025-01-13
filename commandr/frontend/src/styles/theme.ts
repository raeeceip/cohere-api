
export const cohereTheme = {
  colors: {
    primary: {
      DEFAULT: '#6B4FBB',
      light: '#9F8AE5',
      dark: '#4A3880',
      error: '#EF4444',
    },
    background: {
      DEFAULT: '#FFFFFF',
      secondary: '#F5F5F5',
      tertiary: '#FAFAFA',
      dark: '#1A1A1A',
    },
    surface: {
      DEFAULT: '#FFFFFF',
      raised: '#F8F9FA',
      overlay: 'rgba(0, 0, 0, 0.5)',
    },
    text: {
      primary: '#1F2937',
      secondary: '#3f3f3f',
      accent: '#6B4FBB',
      inverted: '#FFFFFF',
    },
    border: {
      DEFAULT: '#E5E7EB',
      light: '#F3F4F6',
      dark: '#D1D5DB',
    },
    status: {
      success: '#10B981',
      error: '#EF4444',
      warning: '#F59E0B',
      info: '#3B82F6',
    }
  },
  spacing: {
    xs : '0.25rem',
     sm : '0.5rem',
      md : '1rem',
      lg : '1.5rem',
      xl : '2rem',
      '2xl' : '3rem',
      '3xl' : '4rem',
      '4xl' : '6rem',
      full : '100%',
  },
  radii: {
    sm: '0.375rem',
    md: '0.5rem',
    lg: '0.75rem',
    xl: '1rem',
    '2xl': '1.5rem',
    full: '9999px',
  },
  shadows: {
    sm: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
    md: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
    lg: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
  },

  warning : {
    DEFAULT: '#F59E0B',
    light: '#FEF3C7',
    dark: '#92400E',
  },
}

export type cohereTheme= typeof cohereTheme