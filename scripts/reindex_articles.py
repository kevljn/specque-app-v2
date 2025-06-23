import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app, db
from app.models.legislative import LegislativeText, LegalElement
from docx import Document

app = create_app()

def create_element(legislative_text_id, type_, index, title, content, parent=None):
    el = LegalElement(
        legislative_text_id=legislative_text_id,
        type=type_,
        index=index,
        title=title,
        content=content,
        parent=parent
    )
    db.session.add(el)
    db.session.flush()  # pour avoir l'id
    return el

with app.app_context():
    text = LegislativeText.query.get(6)
    if not text:
        print('Texte id=6 introuvable')
        sys.exit(1)
    # Nettoyage des anciens éléments
    LegalElement.query.filter_by(legislative_text_id=text.id).delete()
    db.session.commit()

    # Parse le .docx fourni (doit être à la racine)
    doc = Document('SPECQUE 2025.S00X(COD) - RADITS_FINAL.docx')
    current_parent = None
    current_article = None
    current_paragraph = None
    current_alinea = None
    current_annexe = None
    # Ce parsing est simplifié, il faudra l'adapter selon la structure réelle du docx
    for para in doc.paragraphs:
        txt = para.text.strip()
        if not txt:
            continue
        # Titre principal
        if para.style.name.startswith('Title'):
            current_parent = create_element(text.id, 'titre', None, txt, None)
        # Préambule
        elif txt.lower().startswith('préambule'):
            current_parent = create_element(text.id, 'preambule', None, txt, None)
        # Annexe
        elif txt.lower().startswith('annexe'):
            current_annexe = create_element(text.id, 'annexe', None, txt, None)
        # Article
        elif txt.lower().startswith('article'):
            idx = txt.split()[1].replace('.', '') if len(txt.split()) > 1 else None
            current_article = create_element(text.id, 'article', idx, txt, None, parent=current_parent)
            current_paragraph = None
            current_alinea = None
        # Paragraphe (numérotation classique)
        elif txt[:2].isdigit() and txt[2] == '.':
            idx = txt[:2].strip('. ')
            current_paragraph = create_element(text.id, 'paragraphe', idx, None, txt, parent=current_article)
            current_alinea = None
        # Alinéa (ex: tiret, lettre, etc.)
        elif txt[0] in ['-', '•', '*'] or (txt[0].isalpha() and txt[1:3] == ') '):
            idx = txt[:2].strip('. )')
            current_alinea = create_element(text.id, 'alinea', idx, None, txt, parent=current_paragraph or current_article)
        # Point (ex: a), 1), i), etc.)
        elif (txt[0].isalpha() and txt[1] == ')') or (txt[0].isdigit() and txt[1] == ')'):
            idx = txt[:2].strip('. )')
            create_element(text.id, 'point', idx, None, txt, parent=current_alinea or current_paragraph or current_article)
        # Appendice
        elif txt.lower().startswith('appendice'):
            create_element(text.id, 'appendice', None, txt, None, parent=current_annexe)
        # Sinon, rattacher au parent courant
        else:
            create_element(text.id, 'texte', None, None, txt, parent=current_alinea or current_paragraph or current_article or current_parent)
    db.session.commit()
    print('Migration et découpage terminés pour le texte 6.') 