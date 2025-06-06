import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-w', '--web', help=f'Path to pdf.js distributed web/ folder, end without `/`', type=str)
parser.add_argument('-v', '--viewer', help=f'Path to extension viewer/ folder, end without `/`', type=str)
args = parser.parse_args()

with open(args.web + '/viewer.html', 'rt', encoding='utf-8') as fin:
    with open(args.viewer + '/viewer.html', 'wt', encoding='utf-8') as fout:
        for line in fin:
            fout.write(
                line.replace('''<title>PDF.js viewer</title>''', '''<meta http-equiv="Content-Security-Policy" content="default-src 'self'; base-uri 'none'; connect-src 'self' ws://127.0.0.1:*; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob:;">\n    <title>PDF.js viewer</title>''')
                    .replace('''<link rel="stylesheet" href="viewer.css">''', '''<link rel="stylesheet" href="viewer.css">\n    <link rel="stylesheet" href="latexworkshop.css">''')
                    .replace('''<script src="../build/pdf.mjs" type="module"></script>''', '''<script src="build/pdf.mjs" type="module"></script>''')
                    .replace('''<script src="viewer.mjs" type="module"></script>''', '''<script src="out/viewer/latexworkshop.js" type="module"></script>''')
                    .replace('''<div class="toolbar">''', '''<div class="toolbar hide">''')
                    .replace('''<div class="toolbarButtonSpacer"></div>''', '''<!-- <div class="toolbarButtonSpacer"></div> -->''')
            )

with open(args.web + '/viewer.mjs', 'rt', encoding='utf-8') as fin:
    with open(args.viewer + '/viewer.mjs', 'wt', encoding='utf-8') as fout:
        currentClass = ''
        for line in fin:
            line = line.replace('''const MATCH_SCROLL_OFFSET_TOP = -50;''', '''const MATCH_SCROLL_OFFSET_TOP = -100;''') \
                .replace('''this.switchView(view, true);''', '''this.switchView(view, false);''') \
                .replace('''console.warn(`[fluent] Missing translations in ${locale}: ${ids}`);''', '''// console.warn(`[fluent] Missing translations in ${locale}: ${ids}`);''') \
                .replace('''this.removePageBorders = options.removePageBorders || false;''', '''this.removePageBorders = options.removePageBorders || true;''') \
                .replace('''localStorage.setItem("pdfjs.history", databaseStr);''', '''// localStorage.setItem("pdfjs.history", databaseStr);''') \
                .replace('''return localStorage.getItem("pdfjs.history");''', '''return // localStorage.getItem("pdfjs.history");''') \
                .replace('''this.setTitle(title || url);''', '''// this.setTitle(title || url);''') \
                .replace('''localStorage.setItem("pdfjs.preferences", JSON.stringify(prefObj));''', '''// localStorage.setItem("pdfjs.preferences", JSON.stringify(prefObj));''') \
                .replace('''prefs: JSON.parse(localStorage.getItem("pdfjs.preferences"))''', '''prefs: undefined // JSON.parse(localStorage.getItem("pdfjs.preferences"))''') \
                .replace('''(!event.shiftKey || window.chrome || window.opera)) {''', '''(!event.shiftKey || window.chrome || window.opera)) {\n    if (window.parent !== window) {\n      return;\n    }''') \
                .replace('''console.error("webviewerloaded:", ex);''', '''// console.error("webviewerloaded:", ex);''') \
                .replace('''//# sourceMappingURL=viewer.mjs.map''', '''''') \
                .replace('''console.log(`PDF ${pdfDocument.''', '''// console.log(`PDF ${pdfDocument.''') \
                .replace('''value: "../build/pdf.worker.mjs"''', '''value: "./build/pdf.worker.mjs"''') \
                .replace('''value: "../build/pdf.sandbox.mjs"''', '''value: "./build/pdf.sandbox.mjs"''') \
                .replace('''value: "../web/standard_fonts/"''', '''value: "../standard_fonts/"''') \
                .replace('''value: "../web/cmaps/"''', '''value: "../cmaps/"''') \
                .replace('''(this.container.clientWidth - hPadding) / currentPage.width * currentPage.scale / this.#pageWidthScaleFactor;''', '''(this.container.clientWidth - hPadding) / Math.max(...this._pages.map(p => p.width)) * currentPage.scale / this.#pageWidthScaleFactor * (1 / (1 - (viewerTrim ?? 0) / 100));''') \
                .replace('''(this.container.clientHeight - vPadding) / currentPage.height * currentPage.scale;''', '''(this.container.clientHeight - vPadding) / Math.max(...this._pages.map(p => p.height)) * currentPage.scale * (1 / (1 - (viewerTrim ?? 0) / 100));''') \
                .replace('''setRotation(this.initialRotation);''', '''// setRotation(this.initialRotation);''') \
                .replace('''this.pdfLinkService.setHash(this.initialBookmark);''', '''// this.pdfLinkService.setHash(this.initialBookmark);''') \
                .replace('''hPadding = vPadding = 0;''', '''if (this._scrollMode === ScrollMode.HORIZONTAL || this._spreadMode === SpreadMode.NONE) { hPadding = vPadding = 0; } else { hPadding = 10; vPadding = 0; }''') \
                .replace(''' eventBus._on("openfile"''', ''' // eventBus._on("openfile"''') \
                .replace(''' eventBus._on("print"''', ''' // eventBus._on("print"''') \
                .replace(''' eventBus._on("download"''', ''' // eventBus._on("download"''')
            fout.write(line)

os.system(f'git diff --no-index {args.web}/viewer.html {args.viewer}/viewer.html > {args.viewer}/../dev/viewer/viewer.html.diff')
os.system(f'git diff --no-index {args.web}/viewer.mjs {args.viewer}/viewer.mjs > {args.viewer}/../dev/viewer/viewer.mjs.diff')