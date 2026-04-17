# Archivo: arbol_AVL_implementacion.py
# Nombre: Martín Ariza (2251516) - Ivanna Alvarez (225805) - Juliana Rueda (225801)


# ──────────────────────────────────────────
# CLASE NODO
# ──────────────────────────────────────────

class Nodo:
    """
    Representa un nodo dentro del árbol AVL.
    Cada nodo guarda un valor, apunta a sus hijos
    y recuerda su propia altura (para calcular el balance).
    """

    def __init__(self, valor):
        self.valor = valor          # El dato que almacena el nodo
        self.izquierdo = None       # Hijo izquierdo (valores menores)
        self.derecho = None         # Hijo derecho (valores mayores)
        self.altura = 1             # Un nodo nuevo siempre tiene altura 1


# ──────────────────────────────────────────
# CLASE ÁRBOL AVL
# ──────────────────────────────────────────

class ArbolAVL:
    """
    Implementación completa de un árbol AVL.
    Soporta inserción, eliminación, recorridos y visualización.
    """

    def __init__(self):
        self.raiz = None  # El árbol empieza vacío


    # ── Funciones auxiliares ────────────────

    def _altura(self, nodo):
        """
        Devuelve la altura de un nodo.
        Si el nodo es None (no existe), su altura es 0.
        """
        if nodo is None:
            return 0
        return nodo.altura

    def _actualizar_altura(self, nodo):
        """
        Recalcula la altura de un nodo basándose en sus hijos.
        La altura es 1 + el máximo entre la altura del hijo izquierdo
        y la altura del hijo derecho.
        """
        nodo.altura = 1 + max(self._altura(nodo.izquierdo),
                              self._altura(nodo.derecho))

    def _factor_balance(self, nodo):
        """
        Calcula el factor de balance de un nodo.
        Factor = altura(izquierdo) - altura(derecho)
        """
        if nodo is None:
            return 0
        return self._altura(nodo.izquierdo) - self._altura(nodo.derecho)


    # ── Rotaciones ──────────────────────────

    def _rotar_derecha(self, y):
        """
        Rotación simple a la derecha.
        Se usa cuando el subárbol izquierdo está muy cargado.
        """
        x = y.izquierdo
        T2 = x.derecho

        # Realizamos la rotación
        x.derecho = y
        y.izquierdo = T2

        # Actualizamos alturas (primero y, luego x, porque y quedó abajo)
        self._actualizar_altura(y)
        self._actualizar_altura(x)

        return x  # x es la nueva raíz de este subárbol

    def _rotar_izquierda(self, x):
        """
        Rotación simple a la izquierda.
        Se usa cuando el subárbol derecho está muy cargado.
        """
        y = x.derecho
        T2 = y.izquierdo

        # Realizamos la rotación
        y.izquierdo = x
        x.derecho = T2

        # Actualizamos alturas (primero x, luego y, porque x quedó abajo)
        self._actualizar_altura(x)
        self._actualizar_altura(y)

        return y  # y es la nueva raíz de este subárbol

    def _balancear(self, nodo):
        """
        Revisa si un nodo está desbalanceado y aplica la rotación correcta.
        Hay 4 casos posibles:
          1. Izquierda-Izquierda  → rotación derecha simple
          2. Derecha-Derecha      → rotación izquierda simple
          3. Izquierda-Derecha    → rotación izquierda en hijo + rotación derecha
          4. Derecha-Izquierda    → rotación derecha en hijo + rotación izquierda
        """
        self._actualizar_altura(nodo)
        balance = self._factor_balance(nodo)

        # Caso 1: Izquierda-Izquierda
        if balance > 1 and self._factor_balance(nodo.izquierdo) >= 0:
            return self._rotar_derecha(nodo)

        # Caso 2: Derecha-Derecha
        if balance < -1 and self._factor_balance(nodo.derecho) <= 0:
            return self._rotar_izquierda(nodo)

        # Caso 3: Izquierda-Derecha
        if balance > 1 and self._factor_balance(nodo.izquierdo) < 0:
            nodo.izquierdo = self._rotar_izquierda(nodo.izquierdo)
            return self._rotar_derecha(nodo)

        # Caso 4: Derecha-Izquierda
        if balance < -1 and self._factor_balance(nodo.derecho) > 0:
            nodo.derecho = self._rotar_derecha(nodo.derecho)
            return self._rotar_izquierda(nodo)

        # Si no hay desbalance, devolvemos el nodo sin cambios
        return nodo


    # ── Inserción ───────────────────────────

    def insertar(self, valor):
        """Inserta un valor en el árbol AVL."""
        self.raiz = self._insertar_recursivo(self.raiz, valor)

    def _insertar_recursivo(self, nodo, valor):
        """
        Función interna que inserta de forma recursiva.
        Primero hace la inserción normal de un BST,
        luego balancea el camino de regreso.
        """
        # Caso base: llegamos a un lugar vacío, creamos el nodo
        if nodo is None:
            return Nodo(valor)

        # Insertamos en el subárbol correcto según el valor
        if valor < nodo.valor:
            nodo.izquierdo = self._insertar_recursivo(nodo.izquierdo, valor)
        elif valor > nodo.valor:
            nodo.derecho = self._insertar_recursivo(nodo.derecho, valor)
        else:
            # Valor duplicado: no hacemos nada (el árbol no admite duplicados)
            return nodo

        # Al regresar de la recursión, balanceamos este nodo
        return self._balancear(nodo)


    # ── Eliminación ─────────────────────────

    def eliminar(self, valor):
        """Elimina un valor del árbol AVL."""
        self.raiz = self._eliminar_recursivo(self.raiz, valor)

    def _eliminar_recursivo(self, nodo, valor):
        """
        Función interna que elimina de forma recursiva.
        Tiene 3 casos para la eliminación:
          1. El nodo no tiene hijos → simplemente lo borramos
          2. El nodo tiene un hijo → lo reemplazamos por ese hijo
          3. El nodo tiene dos hijos → lo reemplazamos por su sucesor inorden
        """
        # Si el nodo no existe, no hay nada que eliminar
        if nodo is None:
            return nodo

        # Buscamos el nodo a eliminar
        if valor < nodo.valor:
            nodo.izquierdo = self._eliminar_recursivo(nodo.izquierdo, valor)
        elif valor > nodo.valor:
            nodo.derecho = self._eliminar_recursivo(nodo.derecho, valor)
        else:
            # Encontramos el nodo a eliminar
            if nodo.izquierdo is None:
                # Caso 1 y 2: sin hijo izquierdo
                return nodo.derecho
            elif nodo.derecho is None:
                # Caso 2: sin hijo derecho
                return nodo.izquierdo
            else:
                # Caso 3: tiene dos hijos
                # Buscamos el sucesor inorden (el mínimo del subárbol derecho)
                sucesor = self._minimo(nodo.derecho)
                # Copiamos el valor del sucesor en este nodo
                nodo.valor = sucesor.valor
                # Eliminamos el sucesor del subárbol derecho
                nodo.derecho = self._eliminar_recursivo(nodo.derecho, sucesor.valor)

        # Balanceamos al regresar
        return self._balancear(nodo)

    def _minimo(self, nodo):
        """
        Encuentra el nodo con el valor mínimo en un subárbol.
        En un BST, el mínimo siempre está en el extremo izquierdo.
        """
        actual = nodo
        while actual.izquierdo is not None:
            actual = actual.izquierdo
        return actual


    # ── Recorridos ──────────────────────────

    def inorden(self):
        """
        Recorrido inorden: izquierdo → raíz → derecho.
        En un BST/AVL esto devuelve los valores ordenados de menor a mayor.
        """
        resultado = []
        self._inorden_recursivo(self.raiz, resultado)
        return resultado

    def _inorden_recursivo(self, nodo, resultado):
        if nodo is not None:
            self._inorden_recursivo(nodo.izquierdo, resultado)
            resultado.append(nodo.valor)
            self._inorden_recursivo(nodo.derecho, resultado)

    def preorden(self):
        """
        Recorrido preorden: raíz → izquierdo → derecho.
        Útil para copiar o serializar el árbol.
        """
        resultado = []
        self._preorden_recursivo(self.raiz, resultado)
        return resultado

    def _preorden_recursivo(self, nodo, resultado):
        if nodo is not None:
            resultado.append(nodo.valor)
            self._preorden_recursivo(nodo.izquierdo, resultado)
            self._preorden_recursivo(nodo.derecho, resultado)

    def postorden(self):
        """
        Recorrido postorden: izquierdo → derecho → raíz.
        Útil para eliminar el árbol o evaluar expresiones.
        """
        resultado = []
        self._postorden_recursivo(self.raiz, resultado)
        return resultado

    def _postorden_recursivo(self, nodo, resultado):
        if nodo is not None:
            self._postorden_recursivo(nodo.izquierdo, resultado)
            self._postorden_recursivo(nodo.derecho, resultado)
            resultado.append(nodo.valor)


    # ── Búsqueda ────────────────────────────

    def buscar(self, valor):
        """
        Busca un valor en el árbol.
        Devuelve True si lo encuentra, False si no.
        """
        return self._buscar_recursivo(self.raiz, valor)

    def _buscar_recursivo(self, nodo, valor):
        if nodo is None:
            return False
        if valor == nodo.valor:
            return True
        elif valor < nodo.valor:
            return self._buscar_recursivo(nodo.izquierdo, valor)
        else:
            return self._buscar_recursivo(nodo.derecho, valor)


    # ── Visualización ───────────────────────

    def visualizar(self):
        """
        Imprime el árbol de forma visual en la consola.
        Muestra la estructura con indentación para ver los niveles.
        Cada nodo muestra su valor y su factor de balance entre paréntesis.
        """
        if self.raiz is None:
            print("El árbol está vacío.")
            return
        print("Árbol AVL (valor [balance]):")
        print("─" * 40)
        self._visualizar_recursivo(self.raiz, "", True)
        print("─" * 40)

    def _visualizar_recursivo(self, nodo, prefijo, es_derecho):
        """
        Función auxiliar que imprime el árbol rotado 90°.
        Los nodos de la derecha aparecen arriba y los de la izquierda abajo.
        """
        if nodo is not None:
            # Primero imprimimos el subárbol derecho (aparece arriba)
            self._visualizar_recursivo(
                nodo.derecho,
                prefijo + ("    " if es_derecho else "│   "),
                True
            )

            # Imprimimos el nodo actual con su factor de balance
            balance = self._factor_balance(nodo)
            print(prefijo + ("└── " if es_derecho else "┌── ") +
                  f"{nodo.valor} [{balance:+d}]")

            # Luego imprimimos el subárbol izquierdo (aparece abajo)
            self._visualizar_recursivo(
                nodo.izquierdo,
                prefijo + ("    " if not es_derecho else "│   "),
                False
            )


# ──────────────────────────────────────────
# EJEMPLO DE USO
# ──────────────────────────────────────────

if __name__ == "__main__":

    print("=" * 50)
    print("   DEMO: Árbol AVL")
    print("=" * 50)

    arbol = ArbolAVL()

    # Insertamos algunos valores
    valores = [30, 20, 40, 10, 25, 35, 50, 5, 15]
    print(f"\nInsertando valores: {valores}")
    for v in valores:
        arbol.insertar(v)

    # Visualizamos el árbol
    print()
    arbol.visualizar()

    # Recorridos
    print(f"\nInorden   (ordenado): {arbol.inorden()}")
    print(f"Preorden  (raíz primero): {arbol.preorden()}")
    print(f"Postorden (raíz al final): {arbol.postorden()}")

    # Búsqueda
    print(f"\nBuscar 25: {arbol.buscar(25)}")
    print(f"Buscar 99: {arbol.buscar(99)}")

    # Eliminación
    print("\nEliminando el valor 20...")
    arbol.eliminar(20)
    print()
    arbol.visualizar()
    print(f"Inorden después de eliminar 20: {arbol.inorden()}")

    print("\nEliminando la raíz (30)...")
    arbol.eliminar(30)
    print()
    arbol.visualizar()
    print(f"Inorden después de eliminar 30: {arbol.inorden()}")

    print("\nFin del demo.")
