from flask import Flask, render_template, request

app = Flask(__name__)

tax_bands = [(0, 5100, 0), (5101, 7100, 0.2), (7101, 9200, 0.3), (9201, float('inf'), 0.37)]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    gross_amount = float(request.form['gross_amount'])
    remaining_amount = gross_amount
    tax_breakdown = []

    for lower, upper, rate in tax_bands:
        if gross_amount <= lower:
            break
        elif gross_amount > upper:
            taxable_amount = upper - lower
            tax = taxable_amount * rate
            remaining_amount -= tax
            tax_breakdown.append((f"{lower}-{upper}", taxable_amount, tax))
        else:
            taxable_amount = gross_amount - lower
            tax = taxable_amount * rate
            remaining_amount -= tax
            tax_breakdown.append((f"{lower}-{gross_amount}", taxable_amount, tax))

    return render_template('results.html', gross_amount=gross_amount, tax_breakdown=tax_breakdown, remaining_amount=remaining_amount)

if __name__ == '__main__':
    app.run(debug=True)
