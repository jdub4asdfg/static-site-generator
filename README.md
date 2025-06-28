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
The static site generator supports several text types:
- Normal

- Bold

- Italic

- Code

- Links

- Images

- Headers

- Ordered lists

- Unordered lists

- Quotes

Check out [my source code](https://github.com/jdub4asdfg/static-site-generator/blob/main/content/index.md) if you need any help with writing out the different text types in markdown.

#### Additional stuff to take note of:
The markdown converter does not support nesting text types, meaning you can't do this: `**_bold and italicised text_**`.

The markdown converter parses the markdown file paragraph by paragraph, where paragraphs are separated by a new line, like so:
```
Paragraph 1

Paragraph 2
```

Lastly, always start your markdown files with a `h1` header, any text in this header will be the name of your browser tab.