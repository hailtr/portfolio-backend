export const defaultLocale = 'es';
export const locales = ['es', 'en'] as const;
export type Locale = (typeof locales)[number];

/** Get current locale from Astro.currentLocale or fallback */
export function getLocale(astroLocale: string | undefined): Locale {
  if (astroLocale === 'en') return 'en';
  return 'es';
}

/** Build a localized path. ES has no prefix, EN gets /en/ */
export function localePath(path: string, locale: Locale): string {
  const clean = path.startsWith('/') ? path : `/${path}`;
  if (locale === 'es') return clean;
  return `/en${clean}`;
}

/** Get the alternate locale */
export function altLocale(locale: Locale): Locale {
  return locale === 'es' ? 'en' : 'es';
}

const translations = {
  // Nav
  'nav.home': { es: 'Inicio', en: 'Home' },
  'nav.work': { es: 'Trabajo', en: 'Work' },
  'nav.about': { es: 'Sobre mí', en: 'About' },
  'nav.experience': { es: 'Experiencia', en: 'Experience' },
  'nav.caseStudies': { es: 'Casos de Estudio', en: 'Case Studies' },
  'nav.projects': { es: 'Proyectos', en: 'Projects' },
  'nav.contact': { es: 'Contacto', en: 'Contact' },

  // Hero
  'hero.scaffold': { es: 'Sitio en construcción', en: 'Site under construction' },
  'hero.tagline': {
    es: 'Streaming pipelines, lakehouse architectures, y plataformas de datos Microsoft',
    en: 'Streaming pipelines, lakehouse architectures, and Microsoft data platforms',
  },
  'hero.cta.caseStudies': { es: 'Ver casos de estudio', en: 'View case studies' },
  'hero.cta.cv': { es: 'Ver CV', en: 'View CV' },

  // About
  'about.title': { es: 'Acerca de mí', en: 'About me' },
  'about.skills': { es: 'Stack Técnico', en: 'Tech Stack' },

  // Experience
  'experience.title': { es: 'Experiencia', en: 'Experience' },
  'experience.present': { es: 'Presente', en: 'Present' },

  // Projects
  'projects.title': { es: 'Proyectos', en: 'Projects' },

  // Case Studies
  'caseStudies.title': { es: 'Casos de Estudio', en: 'Case Studies' },
  'caseStudies.viewAll': { es: 'Ver todos', en: 'View all' },

  // Contact
  'contact.title': { es: 'Contacto', en: 'Contact' },
  'contact.cta': { es: 'Escríbeme', en: 'Get in touch' },

  // Footer
  'footer.built': { es: 'Construido con', en: 'Built with' },

  // Misc
  'misc.readMore': { es: 'Leer más', en: 'Read more' },
  'misc.backHome': { es: 'Volver al inicio', en: 'Back home' },
} as const;

type TranslationKey = keyof typeof translations;

export function t(key: TranslationKey, locale: Locale): string {
  return translations[key]?.[locale] ?? key;
}
