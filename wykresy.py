  <script>
            const functionStr = "{{ function_str }}";
            #zmienna przechowujaca wyrazenie funkcji

            const derivativeStr = "{{ derivative_str }}";
            #zmienna przechowujaca pochodna

            #inicjalizacja wykresu unckji
            const board1 = JXG.JSXGraph.initBoard('jxgbox1', {
                boundingbox: [-10, 10, 10, -10], #granice wykresu
                axis: true
            });

            #Tworzenie wykresu funkcji za pomocą JSXGraph.
            const graph1 = board1.create('functiongraph', [function(x) {
                return eval(functionStr);
            }]); #eval(functionStr) wykonuje wyrażenie funkcji.

            #inicjalizacja tablicy dla wykresu pochodnej
            const board2 = JXG.JSXGraph.initBoard('jxgbox2', {
                boundingbox: [-10, 10, 10, -10],
                axis: true
            });
            #Tworzenie wykresu pochodnej za pomocą JSXGraph.
            const graph2 = board2.create('functiongraph', [function(x) {
                return eval(derivativeStr); #eval(derivativeStr)
            }]);
        </script>