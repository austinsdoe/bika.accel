This folder contains all the logic and templates for the generation of
custom-stickers for Samples, Analysis Requests, Worksheets, etc.

If no special logic is required, there is only the need to add a .tpl file
inside stickers/templates folder, together with its corresponding .css file.
Both files should have the same name so for a <mystickertemplate>.tpl file you
should add the corresponding <mystickertemplate>.css inside the same directory.

In some cases, you may need additional behavior not supported by the default
Sticker's view from bika.lims (e.g, there are additional fields for Sample
content type that have defined in this specific add-on and one or more of these
fields must be displayed in the sticker). In such a case add a stickers.py file
inside this /stickers and override bika.lims.browser.stickers.Sticker.
