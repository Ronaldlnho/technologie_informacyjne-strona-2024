from flask import Flask, render_template, request
import sympy as sp
import re
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/demonstration', methods=['GET', 'POST'])
def demonstration():
    extrema_points = []
    error_message = None
    accepted_chars = ['0','1','2','3','4','5','6','7','8','9','x','(',')','-','+','/',',','*','^']
    function_str = ""
    derivative_str = ""
    function_latex = ""
    derivative_latex = ""
    if request.method == 'POST':
        try:
            # Pobieranie funkcji z formularza i zamiana '^' na '**'
            input_txt = request.form['function'].replace('^', '**')
            
            function_str = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', input_txt)
            
            
            for i in range(len(function_str)):
                if function_str[i] not in accepted_chars:
                    raise ValueError
                try:
                    if function_str[i] == '/' and function_str[i + 1] == '0' and function_str[i+2] != ',':
                        raise ZeroDivisionError
                except IndexError:
                    if function_str[i] == '/' and function_str[i + 1] == '0':
                        raise ZeroDivisionError
            # Definiowanie zmiennej i funkcji
            x = sp.symbols('x')
            function = sp.sympify(function_str)
            function_latex = sp.latex(function)

            # Liczenie pochodnej
            derivative = sp.diff(function, x)
            derivative_str = str(derivative)
            derivative_latex = sp.latex(derivative)
            if 'x' in function_str:
            # Wyznaczanie ekstremów
                critical_points = sp.solveset(sp.Eq(derivative, 0), x)
                second_derivative = sp.diff(derivative, x)
                extrema_points = []
                for point in critical_points:
                    point_val = point.evalf()
                    function_val = function.subs(x, point).evalf()
                    second_derivative_val = second_derivative.subs(x, point).evalf()
                    if second_derivative_val > 0:
                        extrema_points.append((point_val, function_val, 'minimum'))
                    elif second_derivative_val < 0:
                        extrema_points.append((point_val, function_val, 'maksimum'))
                    else:
                        extrema_points.append((point_val, function_val, 'punkt siodłowy'))

        except ValueError:
            error_message = "Błąd: Wprowadź poprawną wartość liczbową."
        except ZeroDivisionError:
            error_message = "Błąd: Dzielenie przez zero jest niemożliwe."
        except Exception as e:
            error_message = f"Błąd: {str(e)}"

    return render_template('demonstration.html', extrema_points=extrema_points, error_message=error_message, function_str=function_str, derivative_str=derivative_str, function_latex=function_latex, derivative_latex=derivative_latex)

@app.route('/authors')
def authors():
    return render_template('authors.html')

if __name__ == '__main__':
    app.run(debug=True)
