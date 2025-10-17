/**
 * Metro Bundler Configuration
 *
 * Optimized configuration for React Native bundling
 */

const { getDefaultConfig, mergeConfig } = require('@react-native/metro-config');

/**
 * Metro configuration
 * https://facebook.github.io/metro/docs/configuration
 */
const config = {
  transformer: {
    // Use Babel to transform JS
    babelTransformerPath: require.resolve('react-native-svg-transformer'),

    // Inline requires for better performance
    inlineRequires: true,

    // Minifier options
    minifierConfig: {
      keep_classnames: true,
      keep_fnames: true,
      mangle: {
        keep_classnames: true,
        keep_fnames: true,
      },
    },
  },

  resolver: {
    // Asset extensions
    assetExts: [
      'png',
      'jpg',
      'jpeg',
      'gif',
      'webp',
      'svg',
      'ttf',
      'otf',
      'mp4',
      'mov',
    ],

    // Source extensions
    sourceExts: ['js', 'jsx', 'ts', 'tsx', 'json'],

    // Platform-specific extensions (processed in order)
    platforms: ['ios', 'android'],
  },

  // Cache configuration
  cacheStores: [
    {
      name: 'filesystem',
      options: {
        root: '.metro',
      },
    },
  ],

  // Watch configuration
  watchFolders: [],

  // Server configuration
  server: {
    port: 8081,
  },
};

module.exports = mergeConfig(getDefaultConfig(__dirname), config);
