import csv
from fpdf import FPDF
from collections import defaultdict

def read_and_analyze(filename):
    data = []
    department_scores = defaultdict(list)

    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name = row['Name']
            dept = row['Department']
            score = int(row['Score'])
            data.append((name, dept, score))
            department_scores[dept].append(score)

    analysis = {
        dept: {
            'count': len(scores),
            'avg_score': sum(scores) / len(scores)
        }
        for dept, scores in department_scores.items()
    }

    return data, analysis

class PDFReport(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "Automated Internship Report - CodTech", ln=True, align="C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def add_summary(self, analysis):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Department Summary:", ln=True)
        self.set_font("Arial", "", 12)
        for dept, stats in analysis.items():
            self.cell(0, 10, f"{dept}: {stats['count']} interns, Average Score = {stats['avg_score']:.2f}", ln=True)
        self.ln(10)

    def add_details(self, data):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Intern Details:", ln=True)
        self.set_font("Arial", "", 12)
        for name, dept, score in data:
            self.cell(0, 10, f"{name} - {dept} - Score: {score}", ln=True)
        self.ln(10)

    def add_certificate_notice(self, end_date):
        self.set_font("Arial", "B", 12)
        self.set_text_color(220, 50, 50)
        self.multi_cell(0, 10, f"Completion certificate will be issued on your internship end date: {end_date}", align="C")
        self.set_text_color(0, 0, 0)
        self.ln(5)

def generate_pdf(data, analysis, end_date):
    pdf = PDFReport()
    pdf.add_page()
    pdf.add_summary(analysis)
    pdf.add_details(data)
    pdf.add_certificate_notice(end_date)
    pdf.output("Internship_Report.pdf")
    print("✅ PDF report generated: Internship_Report.pdf")

if __name__ == "__main__":
    print("Reading and analyzing data...")
    data, analysis = read_and_analyze("data.csv")
    print("Data read:", data)
    print("Generating PDF...")
    generate_pdf(data, analysis, end_date="31st July 2025")

import os
os.startfile("Internship_Report.pdf")  # Only works on Windows
