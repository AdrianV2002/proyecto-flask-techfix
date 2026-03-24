class ProductoForm:
    @staticmethod
    def procesar_creacion(form_data):
        return {
            'nombre': form_data.get('nombre'),
            'cantidad': int(form_data.get('cantidad', 0)),
            'precio': float(form_data.get('precio', 0.0)),
            'descripcion': form_data.get('descripcion'),
            'imagen': form_data.get('imagen')
        }

    @staticmethod
    def procesar_actualizacion(form_data):
        return {
            'id_prod': int(form_data.get('id_prod')),
            'cantidad': int(form_data.get('cantidad', 0)),
            'precio': float(form_data.get('precio', 0.0))
        }