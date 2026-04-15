import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const caseStudies = defineCollection({
  loader: glob({ pattern: '**/*.mdx', base: './src/content/case-studies' }),
  schema: z.object({
    title: z.object({ es: z.string(), en: z.string() }),
    client: z.string(),
    dates: z.string(),
    location: z.string(),
    metric: z.object({ value: z.string(), label: z.object({ es: z.string(), en: z.string() }) }),
    summary: z.object({ es: z.string(), en: z.string() }),
    stack: z.array(z.string()),
    tags: z.array(z.string()),
    order: z.number().default(0),
  }),
});

export const collections = { 'case-studies': caseStudies };
