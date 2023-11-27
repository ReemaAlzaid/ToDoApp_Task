from fastapi import HTTPException
from fpdf import FPDF

async def create_pdf(title:str,text:any,owner:str):
    pdf = FPDF()
    
    pdf.add_page()
    
    pdf.set_font("Arial", size = 15)

    pdf.cell(200, 10, txt = owner+" List", 
            ln = 2, align = 'C')
    
    pdf.set_font("Arial", size = 11)
    with pdf.table(borders_layout="MINIMAL") as table:
        row = table.row()
        row.cell(text="Task",align = 'C')
        row.cell(text="Status",align = 'C')
        for item in text:
                row = table.row()
                row.cell(text=item.title,align = 'C')
                row.cell(text=item.status,align = 'C')

    return pdf.output(".\\static\\"+title+".pdf") 