
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.db import transaction

from .models import Producto, Cliente, Proveedor, Venta, DetalleVenta
from .forms import ProductoForm, ClienteForm, ProveedorForm


def inicio(request):
    return render(request, "ventas/inicio.html")


def registro(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect("inicio")
    else:
        form = UserCreationForm()

    return render(request, "ventas/registro.html", {"form": form})


def iniciar_sesion(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("inicio")
    else:
        form = AuthenticationForm()

    return render(request, "ventas/login.html", {"form": form})


def cerrar_sesion(request):
    logout(request)
    return redirect("login")


def productos(request):
    lista_productos = Producto.objects.all()
    return render(
        request, "ventas/productos.html",
        {"productos": lista_productos}
    )


def crear_producto(request):
    if request.method == "POST":
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto registrado correctamente.")
            return redirect("productos")
    else:
        form = ProductoForm()

    return render(request, "ventas/crear_producto.html", {"form": form})


def editar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)

    if request.method == "POST":
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto actualizado correctamente.")
            return redirect("productos")
    else:
        form = ProductoForm(instance=producto)

    return render(
        request, "ventas/editar_producto.html",
        {"form": form, "producto": producto}
    )


def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)

    if request.method == "POST":
        producto.delete()
        messages.success(request, "Producto eliminado correctamente.")
        return redirect("productos")

    return render(
        request, "ventas/eliminar_producto.html",
        {"producto": producto}
    )


def clientes(request):
    lista_clientes = Cliente.objects.all()
    return render(
        request, "ventas/clientes.html",
        {"clientes": lista_clientes}
    )


def crear_cliente(request):
    if request.method == "POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cliente registrado correctamente.")
            return redirect("clientes")
    else:
        form = ClienteForm()

    return render(request, "ventas/crear_cliente.html", {"form": form})


def proveedores(request):
    lista_proveedores = Proveedor.objects.all()
    return render(
        request, "ventas/proveedores.html",
        {"proveedores": lista_proveedores}
    )


def crear_proveedor(request):
    if request.method == "POST":
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Proveedor registrado correctamente.")
            return redirect("proveedores")
    else:
        form = ProveedorForm()

    return render(request, "ventas/crear_proveedor.html", {"form": form})


def ventas(request):
    lista_ventas = Venta.objects.select_related("cliente").order_by("-fecha")
    return render(
        request, "ventas/ventas.html",
        {"ventas": lista_ventas}
    )


def crear_venta(request):
    lista_productos = Producto.objects.all()

    if request.method == "POST":
        nombre_cliente = request.POST.get("cliente", "").strip()
        producto_id = request.POST.get("producto", "").strip()
        cantidad_texto = request.POST.get("cantidad", "").strip()

        if not nombre_cliente:
            messages.error(request, "Escribe el nombre del cliente.")
        elif not producto_id:
            messages.error(request, "Selecciona un producto.")
        else:
            try:
                cantidad = int(cantidad_texto)

                if cantidad <= 0:
                    messages.error(
                        request, "La cantidad debe ser mayor que cero."
                    )
                else:
                    producto = get_object_or_404(
                        Producto, pk=producto_id
                    )

                    if cantidad > producto.cantidad:
                        messages.error(
                            request,
                            "No hay suficiente inventario para esa venta."
                        )
                    else:
                        with transaction.atomic():
                            cliente = Cliente.objects.filter(
                                nombre__iexact=nombre_cliente
                            ).first()

                            if cliente is None:
                                cliente = Cliente.objects.create(
                                    nombre=nombre_cliente
                                )

                            venta = Venta.objects.create(cliente=cliente)

                            DetalleVenta.objects.create(
                                venta=venta,
                                producto=producto,
                                cantidad=cantidad,
                                precio_unitario=producto.precio
                            )

                            producto.cantidad -= cantidad
                            producto.save()

                        messages.success(
                            request, "Venta registrada correctamente."
                        )
                        return redirect("ventas")

            except (ValueError, TypeError):
                messages.error(request, "Escribe una cantidad válida.")

    return render(
        request, "ventas/crear_venta.html",
        {"productos": lista_productos}
    )
