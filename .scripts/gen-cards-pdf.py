from fpdf import FPDF
import os, json, sys

CARD_SIZE = (69, 94) # in mm (size of the card with the bleed line)

path = os.environ.get('DECK_PATH', os.path.pardir)
if not os.path.isabs(path):
    path = os.path.join(os.path.dirname(__file__), path)

outpath = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), os.path.pardir, 'build')
if not os.path.isabs(outpath):
    outpath = os.path.join(os.curdir, outpath)

with open(os.path.join(path, 'deck.json'), "r") as file:
    meta = json.load(file)

pdf = FPDF(orientation='L', unit='mm', format='a4')
pdf.set_margins(5,5,5)

tot_cards = len(meta['cards'])
page_size = (int(pdf.epw), int(pdf.h - pdf.t_margin*2))

cards_per_page = (page_size[0] // CARD_SIZE[0], page_size[1] // CARD_SIZE[1])

c = 0
while c < tot_cards:
    pdf.add_page()
    for y in range(cards_per_page[1]):
        y_pos = pdf.t_margin+y*page_size[1]/cards_per_page[1]
        for x in range(cards_per_page[0]):
            x_pos = pdf.l_margin+x*page_size[0]/cards_per_page[0]

            pdf.line(x1=x_pos-1, x2=x_pos+CARD_SIZE[0]+1, y1=y_pos+3, y2=y_pos+3) # top
            pdf.line(x1=x_pos-1, x2=x_pos+CARD_SIZE[0]+1, y1=y_pos+CARD_SIZE[1]-3, y2=y_pos+CARD_SIZE[1]-3) # bottom
            pdf.line(y1=y_pos-1, y2=y_pos+CARD_SIZE[1]+1, x1=x_pos+3, x2=x_pos+3) # left
            pdf.line(y1=y_pos-1, y2=y_pos+CARD_SIZE[1]+1, x1=x_pos+CARD_SIZE[0]-3, x2=x_pos+CARD_SIZE[0]-3) # right

            print(os.path.join(path, 'Visuals', meta['cards'][c]['image']))
            pdf.image(os.path.join(path, 'Visuals', meta['cards'][c]['image']), w=CARD_SIZE[0], x=x_pos, y=y_pos)
            c+=1
            if c >= tot_cards:
                break

os.makedirs(outpath, exist_ok=True)
pdf.output(os.path.join(outpath, 'deck.pdf'))