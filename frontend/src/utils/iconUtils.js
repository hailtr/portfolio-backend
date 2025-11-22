/**
 * Icon utility for normalizing and managing skill icons
 * Uses local SVG files OR inline SVG code (preferred)
 * Priority: Inline SVG > Local file
 */

import { getInlineSvg, hasInlineSvg } from "./svgIcons";

// Map skill names to Simple Icons slug names
// Simple Icons uses lowercase with hyphens: https://simpleicons.org/
const SIMPLE_ICONS_MAP = {
  // Languages
  Python: "python",
  SQL: "mysql", // SQL uses mysql icon
  R: "r",
  JavaScript: "javascript",
  Java: "java",

  // Data Tools
  Pandas: "pandas",
  NumPy: "numpy",
  DAX: "microsoftpowerbi", // DAX is Power BI specific
  "Power BI": "microsoftpowerbi",
  Tableau: "tableau",
  Excel: "microsoftexcel",
  TensorFlow: "tensorflow",
  "Scikit-learn": "scikitlearn",
  PostgreSQL: "postgresql",
  MongoDB: "mongodb",
  Supabase: "supabase",

  // Web Stack
  React: "react",
  Flask: "flask",
  Django: "django",
  HTML: "html5",
  CSS: "css3",

  // Cloud & Infrastructure
  Docker: "docker",
  Azure: "microsoftazure",
  Kubernetes: "kubernetes",
  "Google Cloud": "googlecloud",

  // Methodologies
  Git: "git",
  MLOps: "mlflow", // Using MLflow as closest match for MLOps
  "Data Modeling": "postgresql", // Using PostgreSQL icon as database representation
  Agile: "jira", // Using Jira as Agile tool representation
};

// Local icons that exist in /public/svg/
const LOCAL_ICONS = {
  python: "/svg/python.svg",
  sql: "/svg/sql.svg",
  r: "/svg/r.svg",
  javascript: "/svg/javascript.svg",
  java: "/svg/java.svg",
  powerbi: "/svg/powerbi.svg",
  microsoftpowerbi: "/svg/powerbi.svg",
  dax: "/svg/powerbi.svg", // DAX uses Power BI icon
  tableau: "/svg/tableau.svg",
  excel: "/svg/excel.svg",
  microsoftexcel: "/svg/excel.svg",
  postgresql: "/svg/postgresql.svg",
  mongodb: "/svg/mongodb.svg",
  supabase: "/svg/supabase.svg",
  django: "/svg/django-logo-negative.svg",
  css: "/svg/css.svg",
  css3: "/svg/css.svg",
  docker: "/svg/docker.svg",
  azure: "/svg/azure.svg",
  microsoftazure: "/svg/azure.svg",
  git: "/svg/git.svg",
};

/**
 * Normalize skill name for local icon lookup
 * Converts "Power BI" -> "powerbi", "Scikit-learn" -> "scikitlearn", etc.
 */
const normalizeForLocal = (skillName) => {
  return skillName.toLowerCase().replace(/\s+/g, "").replace(/-/g, "");
};

/**
 * Get icon URL for a skill name (fallback to local files)
 * Priority: Inline SVG > Local file
 *
 * @param {string} skillName - Name of the skill
 * @returns {string|null} Icon URL or null if not found
 */
export const getIconUrl = (skillName) => {
  // First check if we have inline SVG (preferred)
  if (hasInlineSvg(skillName)) {
    return null; // Return null to indicate inline SVG should be used
  }

  // Fallback to local files
  const normalizedName = normalizeForLocal(skillName);

  if (LOCAL_ICONS[normalizedName]) {
    return LOCAL_ICONS[normalizedName];
  }

  // Check Simple Icons mapping
  const simpleIconSlug = SIMPLE_ICONS_MAP[skillName];

  if (simpleIconSlug) {
    const normalizedSlug = normalizeForLocal(simpleIconSlug);
    if (LOCAL_ICONS[normalizedSlug]) {
      return LOCAL_ICONS[normalizedSlug];
    }
  }

  console.warn(
    `No icon found for: ${skillName}. Add inline SVG to svgIcons.js or file to LOCAL_ICONS`,
  );
  return null;
};

/**
 * Get icon configuration including filter class if needed
 *
 * @param {string} skillName - Name of the skill
 * @param {string|undefined} customFilter - Custom filter class if specified (overrides default white filter)
 * @returns {object} Icon config with url (or null for inline), inlineSvg, and filter
 */
export const getIconConfig = (skillName, customFilter = null) => {
  // Check for inline SVG first (preferred)
  const inlineSvg = getInlineSvg(skillName);

  if (inlineSvg) {
    return {
      url: null,
      inlineSvg: inlineSvg,
      filter: customFilter || "",
    };
  }

  // Fallback to file URL
  const url = getIconUrl(skillName);
  const filter =
    customFilter !== null && customFilter !== undefined
      ? customFilter
      : "filter-white";

  return {
    url,
    inlineSvg: null,
    filter,
  };
};

/**
 * Check if an icon exists (for validation)
 *
 * @param {string} skillName - Name of the skill
 * @returns {boolean} Whether icon is available
 */
export const hasIcon = (skillName) => {
  return getIconUrl(skillName) !== null;
};
