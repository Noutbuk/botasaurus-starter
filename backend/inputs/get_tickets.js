/**
 * @typedef {import('../../frontend/node_modules/botasaurus-controls/dist/index').Controls} Controls
 */

/**
 * @param {Controls} controls
 */
function getInput(controls) {
    controls
        .link('referer', { isRequired: true, defaultValue: "artist" })
        .link('link', { isRequired: true, defaultValue: "location" })
}
