/**
 * Cloudinary Image Transformation Utilities
 * 
 * Provides helpers to transform Cloudinary URLs for different display contexts.
 * All transformations are non-destructive and applied on-the-fly via URL parameters.
 */

/**
 * Predefined transformation strings for different use cases
 */
export const CloudinaryTransforms = {
    // Hero gallery cards: 3:2 aspect ratio (420x280), AI-powered smart cropping
    HERO_CARD: 'c_fill,w_420,h_280,g_auto,q_auto,f_auto',

    // Detail page gallery: Optimized but maintains aspect ratio
    DETAIL_GALLERY: 'w_800,q_auto,f_auto',

    // Large detail view: High quality for zoom modal
    DETAIL_LARGE: 'w_1200,q_auto,f_auto',

    // Thumbnail: Small square for previews
    THUMBNAIL: 'c_thumb,w_200,h_200,g_face,q_auto,f_auto',
};

/**
 * Transform a Cloudinary URL by inserting transformation parameters
 * 
 * @param {string} url - Original Cloudinary image URL
 * @param {string} transform - Transformation string (use CloudinaryTransforms constants)
 * @returns {string} Transformed URL, or original if not a Cloudinary URL
 * 
 * @example
 * transformCloudinaryUrl(
 *   'https://res.cloudinary.com/demo/image/upload/sample.jpg',
 *   CloudinaryTransforms.HERO_CARD
 * )
 * // Returns: 'https://res.cloudinary.com/demo/image/upload/c_fill,w_420,h_280,g_auto,q_auto,f_auto/sample.jpg'
 */
export const transformCloudinaryUrl = (url, transform) => {
    // Return original if no URL provided
    if (!url) return url;

    // Only transform Cloudinary URLs
    if (!url.includes('cloudinary.com')) {
        return url;
    }

    // Check if URL already has transformations
    if (url.includes('/upload/') && url.match(/\/upload\/[^/]+\//)) {
        // URL already has transformations, don't double-transform
        console.warn('Cloudinary URL already has transformations:', url);
        return url;
    }

    try {
        // Insert transformation parameters after '/upload/'
        return url.replace('/upload/', `/upload/${transform}/`);
    } catch (error) {
        console.error('Failed to transform Cloudinary URL:', error);
        return url; // Fallback to original
    }
};

/**
 * Get the appropriate image URL for hero gallery display
 * Applies smart cropping and optimization for card thumbnails
 * 
 * @param {string} imageUrl - Original image URL
 * @returns {string} Transformed URL optimized for hero cards
 */
export const getHeroImageUrl = (imageUrl) => {
    return transformCloudinaryUrl(imageUrl, CloudinaryTransforms.HERO_CARD);
};

/**
 * Get the appropriate image URL for detail page gallery
 * Optimizes size while maintaining original aspect ratio
 * 
 * @param {string} imageUrl - Original image URL
 * @returns {string} Transformed URL optimized for detail gallery
 */
export const getDetailImageUrl = (imageUrl) => {
    return transformCloudinaryUrl(imageUrl, CloudinaryTransforms.DETAIL_GALLERY);
};

/**
 * Get the appropriate image URL for zoom modal
 * High quality for fullscreen viewing
 * 
 * @param {string} imageUrl - Original image URL
 * @returns {string} Transformed URL optimized for large display
 */
export const getZoomImageUrl = (imageUrl) => {
    return transformCloudinaryUrl(imageUrl, CloudinaryTransforms.DETAIL_LARGE);
};
