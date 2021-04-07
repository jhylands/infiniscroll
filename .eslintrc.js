module.exports = {
    "env": {
        "browser": true,
        "node": true,
        "jquery": true,
        "es6": true,
    },
    "extends": "eslint:recommended",
    "parserOptions": {
        "ecmaVersion": 9,
        "sourceType": "module",
        "ecmaFeatures": {
            "jsx": true,
            "modules": true
        }
    },
    "rules": {
        "max-lines-per-function": ["warn", { "max": 20 }],
        "complexity": ["warn", { "max": 15 }],
        "max-params": ["warn", 5],
        "no-unused-vars": "warn",
        "no-use-before-define": "warn",
        "no-tabs": "error",
        "new-cap": ["error", { "newIsCap": true }],
        "max-statements-per-line": "error",
        "max-depth": ["error", 4],
        "no-magic-numbers": "error",
        "no-console": "off",
        "indent": [
            "error",
            2
        ],
        "linebreak-style": [
            "error",
            "unix"
        ],
        "quotes": [
            "warn",
            "double"
        ],
        "semi": [
            "warn",
            "always"
        ]
    },
    "globals":{
      "document": "writable",
    }
};