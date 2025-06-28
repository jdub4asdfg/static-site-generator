# Static site generator

Converts markdown files to their HTML equivalent.

## Setup
Fork the repository then clone it.
`git clone https://github.com/{YOUR_USERNAME}/{NAME_OF_REPO}.git` in your terminal while in the root of your workspace.

## File structure of your site
Should look like this (before running anything):
```
static-site-generator/
├── content/
│   ├── landing_page.md
│   └── subpage/
│       └── subpage.md
└── static/
    ├── images/
    │   └── image.png
    └── style.css
```

`./main.sh` to test your site locally. This copies files and directories from the **content** and **static** directory to the **docs** directory.
Your **docs** directory should look like this now:
```
static-site-generator/
└── docs/
    ├── images/
    │   └── image.png
    ├── landing_page.md
    ├── subpage/
    │   └── subpage.md
    └── style.css
```

`./build.sh` to get your deployment build. Git add, commit and push to deploy your site to Github Pages.

## How to write your markdown files
Static site generator supports several text types:
- Normal

- Bold, using `**`

- Italic, using `_`

- Code, **`** for single line code, **```** for code that spans multiple lines

- Links, using `[Alt text](link)`

- Images, using `![Alt text](/images/{IMAGE_NAME}.{IMAGE_FORMAT})`

- Headers, supports up to `<h6>`, use `#`s and a space before the text

- Ordered lists, like this (Take note of the space before the text, it must be there):
    ```
    1. text
    2. text
    3. text
    ```

- Unordered lists, like this (Take note of the space before the text, it must be there):
    ```
    - text
    - text
    - text
    ```

- Quotes, using `> ` (Take note of the space before the text, it must be there)

### Additional stuff to take note of
The markdown converter does not support nesting text types, meaning you can't do this: `**_bold and italicised text_**`.

The markdown converter parses the markdown file paragraph by paragraph, where paragraphs are separated by a new line, like so:
```
Paragraph 1

Paragraph 2
```

Lastly, always start your markdown files with a `h1` header, any text in this header will be the name of your browser tab.

You can visit [this demo site](https://jdub4asdfg.github.io/static-site-generator/) and take a look at my source code under the **content** directory if you need an example of how to write markdown files.