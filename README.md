# How you could use it

## Setup
Firstly, you would want to fork this repository then clone it into your workspace.
After forking, type: `git clone https://github.com/{YOUR_USERNAME}/{NAME_OF_REPO}.git`, into your terminal while in the root of your workspace.

## Things to take note of

### How it works
When run, the program first copies whatever is in the **static** directory to the **content** directory, it then copies over whatever is in the **content** directory into the **docs** directory, directory for directory, file for file... Except for markdown files, which are converted to their HTML equivalent.

It isn't necessary to have a **docs** directory before running the program, if you don't have one, the program will create one for you.

### File structure of your site
The landing page of your site is a single markdown file in the root of the **content** directory. Any secondary pages should be a single markdown file as well, put into sub-directories in the **content** directory. For example:
```
content/
├── landing_page.md
└── subpage/
    └──subpage.md
```

Linking pages will be covered in the next section.

If you would like to include any images or style your page, you would have to store images in the **static/images** directory and your CSS file in the **static** directory, located in the root of the repository.

### How to write your markdown files
Static site generator supports several text types:
- Normal
- Bold, by surrounding text with double asterisks: `**`
- Italic, by surrounding text with underscores: `-`
- Code, by surrounding text with single backticks for single line code or triple backticks for code that span mulitple lines
- Links, which is done in this format: `[Alt text](link)`
- Images, which is done in this format: `![Alt text](/images/{IMAGE_NAME}.{IMAGE_FORMAT})`
- Headers, which can be done by including any 1 - 6 number of `#` and a space right after, in front of header text
- Ordered lists, which can be done in this format (Take note of the space before the text, it must be there):
    ```
    1. text
    2. text
    3. text
    ```
- Unordered lists, which can be done in this format (Take note of the space before the text, it must be there):
    ```
    - text
    - text
    - text
    ```
- Quotes, by putting: `> `, before the text you want to be quoted (Take note of the space before the text, it must be there)

The markdown converter does not support nesting text types, meaning you can do this: `**bold text** _italicised text_`. but not this: `**_bold and italicised text_**`.

The markdown converter parses the markdown file paragraph by paragraph, where paragraphs are seperated by a new line, like so:
```
Paragraph 1

Paragraph 2
```

Each paragraph will be converted to a `<div>` in HTML.

Always start your markdown files with a `h1` header, any text in this header will be the name of your browser tab.

Take for example this file structure:
```
content/
├── landing_page.md
└── subpage/
    └──subpage.md
```

To link your subpage from your landing page, anywhere you would like in your markdown file, include for example: `[Read my blog here!](/subpage)`. Clicking on this link on your site brings the user to your subpage.

### Once you've finished writing all the content
Your **content** directory should look something like this:
```
content/
├── landing_page.md
├── index.css
└── subpage/
    └──subpage.md
```

Once you have your **content** directory ready, it's time to run the program. Type this into your terminal while in the root of the repository: `./main.sh`. This allows you to test your build locally before deploying to Github pages.

Once you're satisfied with your build, type this into your terminal while in the root of the repository: `./build.sh`. This is your deployment build which anyone can see. Make sure to Git add, commit and push your build to Github, which you can then host on Github pages.