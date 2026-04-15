// Response types matching api.rafaelortiz.dev/api/*

export interface Profile {
  avatar_url: string | null;
  bio: string;
  email: string;
  location: {
    city: string;
    country: string;
    phone: string;
    region: string;
  };
  name: string;
  role: string;
  social: {
    github: string;
    linkedin: string;
    website: string;
  };
  tagline: string;
}

export interface Experience {
  id: number;
  slug: string;
  company: string;
  title: string;
  description: string;
  location: string;
  startDate: string;
  endDate: string | null;
  current: boolean;
  tags: string[];
}

export interface Skill {
  id: number;
  slug: string;
  name: string;
  description: string | null;
  icon_url: string | null;
  proficiency: number;
  category: string;
  category_id: number;
}

export interface Education {
  id: number;
  slug: string;
  institution: string;
  location: string;
  title: string;
  subtitle: string;
  description: string;
  startDate: string;
  endDate: string;
  current: boolean;
  courses: string[];
}

export interface Certification {
  id: number;
  slug: string;
  title: string;
  description: string;
  issuer: string;
  issueDate: string;
  expiryDate: string;
  url: string;
}

export interface ProjectImage {
  url: string;
  type: string;
  caption: string | null;
  order: number;
  thumbnail_url: string | null;
  alt_text: string;
  width: number;
  height: number;
  is_featured: boolean;
}

export interface ProjectUrl {
  type: string;
  url: string;
  label: string;
  order: number;
}

export interface Project {
  id: number;
  slug: string;
  category: string;
  title: string;
  subtitle: string;
  summary: string;
  description: string;
  content: Record<string, unknown>;
  tags: string[];
  images: ProjectImage[];
  urls: ProjectUrl[];
  desktop_image: string | null;
  mobile_image: string | null;
  preview_video: string | null;
  created_at: string;
}
