import type {
  Profile,
  Experience,
  Skill,
  Education,
  Certification,
  Project,
} from './types';

const API_BASE = 'https://api.rafaelortiz.dev/api';

async function fetchJSON<T>(path: string, lang: string = 'es', fallback: T): Promise<T> {
  const url = `${API_BASE}${path}?lang=${lang}`;
  try {
    const res = await fetch(url);
    if (!res.ok) {
      console.error(`API ${res.status}: ${url}`);
      return fallback;
    }
    return res.json() as Promise<T>;
  } catch (err) {
    console.error(`API unreachable: ${url}`, err);
    return fallback;
  }
}

const EMPTY_PROFILE: Profile = {
  avatar_url: null, bio: '', email: '', name: 'Rafael Ortiz', role: 'Data Engineer',
  location: { city: '', country: '', phone: '', region: '' },
  social: { github: 'https://github.com/hailtr', linkedin: 'https://linkedin.com/in/rafaelortizaguilar', website: '' },
  tagline: '',
};

export function fetchProfile(lang?: string) {
  return fetchJSON<Profile>('/profile', lang, EMPTY_PROFILE);
}

export function fetchExperience(lang?: string) {
  return fetchJSON<Experience[]>('/experience', lang, []);
}

export function fetchSkills(lang?: string) {
  return fetchJSON<Skill[]>('/skills', lang, []);
}

export function fetchEducation(lang?: string) {
  return fetchJSON<Education[]>('/education', lang, []);
}

export function fetchCertifications(lang?: string) {
  return fetchJSON<Certification[]>('/certifications', lang, []);
}

export function fetchProjects(lang?: string) {
  return fetchJSON<Project[]>('/projects', lang, []);
}

/** Group skills by category name */
export function groupSkillsByCategory(skills: Skill[]): Map<string, Skill[]> {
  const grouped = new Map<string, Skill[]>();
  for (const skill of skills) {
    const cat = skill.category ?? 'Other';
    if (!grouped.has(cat)) grouped.set(cat, []);
    grouped.get(cat)!.push(skill);
  }
  return grouped;
}
