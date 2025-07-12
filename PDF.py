import fitz  # PyMuPDF

def redact_pdf(input_path, output_path, redactions, annotations):
    doc = fitz.open(input_path)

    for page_num in range(len(doc)):
        page = doc[page_num]

        # Redact specified words
        for word in redactions:
            text_instances = page.search_for(word)
            for inst in text_instances:
                page.add_redact_annot(inst, fill=(0, 0, 0))
        page.apply_redactions()

        # Add annotations
        for ann in annotations:
            if ann['page'] == page_num:
                rects = page.search_for(ann['text'])
                for rect in rects:
                    if ann['type'] == 'highlight':
                        page.add_highlight_annot(rect)
                    elif ann['type'] == 'comment':
                        annot = page.add_text_annot(rect.tl, ann['comment'])
                        annot.update()

    doc.save(output_path)
    print(f"Saved redacted and annotated PDF to: {output_path}")

# Example usage
redactions = ["confidential", "secret"]
annotations = [
    {"page": 0, "text": "important", "type": "highlight"},
    {"page": 1, "text": "review", "type": "comment", "comment": "Please verify this section."}
]

redact_pdf("input.pdf", "output_redacted.pdf", redactions, annotations)


