from flask import Flask, render_template, request
import sympy as sp

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
    function_str = ""
    derivative_str = ""
    function_latex = ""
    derivative_latex = ""
    if request.method == 'POST':
        try:
            # Pobieranie funkcji z formularza i zamiana '^' na '**'
            function_str = request.form['function'].replace('^', '**')

            # Definiowanie zmiennej i funkcji
            x = sp.symbols('x')
            function = sp.sympify(function_str)
            function_latex = sp.latex(function)

            # Liczenie pochodnej
            derivative = sp.diff(function, x)
            derivative_str = str(derivative)
            derivative_latex = sp.latex(derivative)

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
        except sp.SympifyError:
            error_message = "Błąd: Nie można przetworzyć wprowadzonego wyrażenia. Upewnij się, że jest ono poprawne i używaj operatora '**' zamiast '^' do potęgowania."
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
