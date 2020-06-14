import ipywidgets as widgets
from IPython.display import clear_output, display
import matplotlib.pyplot as plt


def create_multiple_choice(description, options, correct, feedback=None, fig=None):
    """
    Crea un ejercicio múltiple choice con radio buttons (sólo una opción correcta)
    :param description: string con la consigna del ejercicio
    :param options: lista de strings con las opciones
    :param correct: string con la opción correcta. debe estar en options
    :param feedback: mensaje a mostrar para cada respuesta
    :param fig: pyplot.Figure con la(s) imágenes a mostrar. puede contener subplots
    :return: Función que al ejecutarla en la notebook, muestra el ejercicio.
    """
    # verificar los tipos de objetos
    assert isinstance(description, str), "description debe ser un string"
    assert isinstance(options, list), "options debe ser una lista"
    assert isinstance(feedback, list), "feedback debe ser una lista"
    assert isinstance(fig, plt.Figure) or fig is None, "fig debe ser None o una pyplot.figure"
    # verificar que la opcion correcta se encuentre entre las opciones
    if correct not in options:
        raise ValueError('''
        correct tiene que estar entre las opciones.
        correct = {}
        options = {}'''.format(correct, options))

    # definir la función que se retornará
    def _f():
        choice = widgets.RadioButtons(
            options=options,
            description='',
            disabled=False,
            layout=widgets.Layout(width='100%')
        )
        # crear el botón de validar
        validate = widgets.Button(
            description='Validar',
            disabled=False,
            button_style='',  # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Click para validar',
            icon=''
        )
        # imprimir la descripcion
        print(description)
        out = widgets.Output()

        def on_click(change):
            if choice.value == correct:
                validate.button_style = 'success'
                validate.icon = 'check'
            else:
                validate.button_style = 'danger'
                validate.icon = 'remove'
            if feedback:
                with out:
                    clear_output()
                    print(feedback[options.index(choice.value)])

        def on_value_change(change):
            validate.icon = ''
            validate.button_style = ''
            with out:
                clear_output()
        # asignar callbacks
        validate.on_click(on_click)
        choice.observe(on_value_change)
        # mostrar los elementos
        if fig:
            display(fig)
            plt.close(fig)  # evita que la figure se plotee dos veces.
        display(choice, validate, out)

    return _f


def create_checkbox(description, options, correct, fig=None):
    """
    Crea un ejercicio múltiple choice con checkboxes (más de una opción correcta).
    :param description: string con la consigna del ejercicio
    :param options: lista de elementos convertibles a str con las opciones a mostrar
    :param correct: lista de elementos convertibles a str con las opciones correctas
    :param fig: pyplot.Figure con la(s) imágenes a mostrar. puede contener subplots
    :return: Función que al ejecutarla en la notebook, muestra el ejercicio.
    """
    # verificar los tipos de objetos
    assert isinstance(description, str), "description debe ser un string"
    assert isinstance(options, list), "options debe ser una lista"
    assert isinstance(correct, list), "correct debe ser una lista"
    assert isinstance(fig, plt.Figure) or fig is None, "fig debe ser None o una pyplot.figure"
    # verificar que las opciones correctas se encuentren entre las opciones
    for opt in correct:
        if opt not in options:
            raise ValueError('''
            correct tiene que estar entre las opciones.
            correct = {}
            options = {}'''.format(correct, options))
    # definir la función que se retornará
    def _f():
        # crear los checkbox
        checkbox = []
        for opt in options:
            checkbox.append(
                widgets.Checkbox(
                    value=False,
                    description=str(opt),
                    disabled=False,
                    indent=False,
                    layout=widgets.Layout(width='100%')
                )
            )
        # crear el botón de validar
        validate = widgets.Button(
            description='Validar',
            disabled=False,
            button_style='',  # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Click para validar',
            icon=''
        )
        # imprimir la descripcion
        print(description)
        out = widgets.Output()

        # definir el callback para on_click
        def on_click(change):
            resultado = True
            for i, opt in enumerate(options):
                if opt in correct:
                    if checkbox[i].value is False:
                        resultado = False
                        break
                else:
                    if checkbox[i].value is True:
                        resultado = False
                        break
            if resultado:
                validate.button_style = 'success'
                validate.icon = 'check'
            else:
                validate.button_style = 'danger'
                validate.icon = 'remove'

        # definir el callback para un cambio de valor de checkbox
        def on_value_change(change):
            validate.icon = ''
            validate.button_style = ''
            with out:
                clear_output()

        # asignar callbacks
        validate.on_click(on_click)
        for cb in checkbox:
            cb.observe(on_value_change)

        # mostrar los elementos
        if fig:
            display(fig)
            plt.close(fig)  # evita que la figure se plotee dos veces.
        for cb in checkbox:
            display(cb)
        display(validate, out)

    return _f



