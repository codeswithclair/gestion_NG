let reservaciones = [];
let editandoId = null;

const form = document.getElementById("reservationForm");
const body = document.getElementById("reservationsBody");
const searchByName = document.getElementById("searchByName");

const nombreInput = document.getElementById("nombre");
const telefonoInput = document.getElementById("telefono");
const fechaInput = document.getElementById("fecha");
const horaInput = document.getElementById("hora");
const personasInput = document.getElementById("personas");
const estadoInput = document.getElementById("estado");
const notaInput = document.getElementById("nota");

const totalToday = document.getElementById("totalToday");
const upcomingCount = document.getElementById("upcomingCount");
const nextReservationLabel = document.getElementById("nextReservationLabel");
const nextReservationTime = document.getElementById("nextReservationTime");

const btnLimpiar = document.getElementById("btnLimpiar");
const btnBack = document.getElementById("btnBack");
const btnExportarPDF = document.getElementById("btnExportarPDF");

function obtenerFechaLocalHoy() {
    const hoy = new Date();
    const year = hoy.getFullYear();
    const month = String(hoy.getMonth() + 1).padStart(2, "0");
    const day = String(hoy.getDate()).padStart(2, "0");
    return `${year}-${month}-${day}`;
}

function formatearFecha(fecha) {
    return fecha || "—";
}

function obtenerFechaRegistro(reservacion) {
    return reservacion.fecha_registro ? reservacion.fecha_registro.slice(0, 10) : "";
}

function formatearHora(hora) {
    if (!hora) return "—";
    return hora.slice(0, 5);
}

function fechaHoraYaPaso(fecha, hora) {
    const fechaHoraSeleccionada = new Date(`${fecha}T${hora}`);
    const ahora = new Date();
    return fechaHoraSeleccionada < ahora;
}

function normalizarTelefono(telefono) {
    return telefono.replace(/\D/g, "").slice(0, 10);
}

function actualizarHoraMinima() {
    if (fechaInput.value === obtenerFechaLocalHoy()) {
        const ahora = new Date();
        const horas = String(ahora.getHours()).padStart(2, "0");
        const minutos = String(ahora.getMinutes()).padStart(2, "0");
        horaInput.min = `${horas}:${minutos}`;
        if (horaInput.value && horaInput.value < horaInput.min) {
            horaInput.value = "";
        }
    } else {
        horaInput.removeAttribute("min");
    }

    validarHoraInput();
}

function validarHoraInput() {
    if (fechaInput.value === obtenerFechaLocalHoy() && horaInput.value && horaInput.value < horaInput.min) {
        horaInput.setCustomValidity("La hora debe ser igual o posterior a la hora actual.");
    } else {
        horaInput.setCustomValidity("");
    }
}

function limpiarFormulario() {
    form.reset();
    editandoId = null;
    actualizarHoraMinima();

    const submitBtn = form.querySelector("button[type='submit']");
    if (submitBtn) submitBtn.textContent = "Guardar reservación";
}

async function cargarReservaciones() {
    try {
        const res = await fetch("/api/reservaciones");
        const data = await res.json();

        reservaciones = Array.isArray(data) ? data : [];
        ordenarReservaciones();

        renderTabla();
        renderCards();

    } catch (err) {
        console.error("Error al cargar reservaciones:", err);
        alert("No se pudieron cargar las reservaciones.");
    }
}

function renderTabla() {
    body.innerHTML = "";

    const filtro = searchByName.value.trim().toLowerCase();

    const filtradas = reservaciones.filter(r => {
        const nombreCompleto = `${r.nombre_cliente} ${r.apellido_cliente || ""}`.toLowerCase();
        return nombreCompleto.includes(filtro);
    });

    filtradas.forEach(r => {
        const tr = document.createElement("tr");

        tr.innerHTML = `
    <td>${formatearFecha(r.fecha)}</td>
    <td>${formatearHora(r.hora)}</td>
    <td>${r.nombre_cliente} ${r.apellido_cliente || ""}</td>
    <td>${r.telefono || "—"}</td>
    <td>${r.no_personas}</td>
    <td>
        <span class="estado-badge estado-${String(r.estado).toLowerCase()}">
            ${r.estado}
        </span>
    </td>
    <td>
        <button class="table-btn table-btn--small" onclick="editarReservacion(${r.id_reservacion})">
            Editar
        </button>
        <button class="table-btn table-btn--danger table-btn--small" onclick="eliminarReservacion(${r.id_reservacion})">
            Eliminar
        </button>
    </td>
`;

        body.appendChild(tr);
    });
}

function ordenarReservaciones() {
    const ahora = new Date();

    reservaciones.sort((a, b) => {
        const fechaHoraA = new Date(`${a.fecha}T${a.hora}`);
        const fechaHoraB = new Date(`${b.fecha}T${b.hora}`);
        const aYaPaso = fechaHoraA < ahora;
        const bYaPaso = fechaHoraB < ahora;

        if (aYaPaso !== bYaPaso) return aYaPaso ? 1 : -1;
        return fechaHoraA - fechaHoraB;
    });
}

function renderCards() {
    const hoy = obtenerFechaLocalHoy();
    const ahora = new Date();

    const registradasHoy = reservaciones.filter(r => obtenerFechaRegistro(r) === hoy);
    totalToday.textContent = registradasHoy.length;

    const hoyReservaciones = reservaciones.filter(r => r.fecha === hoy);

    const proximas = hoyReservaciones.filter(r => {
        const fechaHora = new Date(`${r.fecha}T${r.hora}`);
        const diff = (fechaHora - ahora) / (1000 * 60);
        return diff >= 0 && diff <= 60;
    });

    upcomingCount.textContent = proximas.length;

    const futuras = reservaciones
        .map(r => ({
            ...r,
            fechaHora: new Date(`${r.fecha}T${r.hora}`)
        }))
        .filter(r => r.fechaHora >= ahora)
        .sort((a, b) => a.fechaHora - b.fechaHora);

    if (futuras.length > 0) {
        nextReservationLabel.textContent = `${futuras[0].nombre_cliente} ${futuras[0].apellido_cliente || ""}`;
        nextReservationTime.textContent = `${futuras[0].fecha} • ${formatearHora(futuras[0].hora)}`;
    } else {
        nextReservationLabel.textContent = "Sin próximas";
        nextReservationTime.textContent = "—";
    }
}

form.addEventListener("submit", async function (e) {
    e.preventDefault();

    const payload = {
        no_empleado: parseInt(localStorage.getItem("NO_EMPLEADO")) || 1001,
        nombre_cliente: nombreInput.value.trim(),
        apellido_cliente: "",
        telefono: normalizarTelefono(telefonoInput.value),
        fecha: fechaInput.value,
        hora: horaInput.value.length === 5 ? horaInput.value + ":00" : horaInput.value,
        no_personas: parseInt(personasInput.value),
        estado: estadoInput.value,
        comentarios: notaInput.value.trim()
    };

    if (!payload.nombre_cliente || !payload.telefono || !payload.fecha || !payload.hora || !payload.no_personas || !payload.estado) {
        alert("Completa todos los campos obligatorios.");
        return;
    }

    if (!/^\d{10}$/.test(payload.telefono)) {
        alert("El telefono debe tener exactamente 10 digitos.");
        telefonoInput.focus();
        return;
    }

    if (fechaHoraYaPaso(payload.fecha, payload.hora)) {
        alert("No puedes registrar una reservación en una fecha u hora que ya pasó.");
        return;
    }

    try {
        const url = editandoId ? `/api/reservaciones/${editandoId}` : "/api/reservaciones";
        const metodo = editandoId ? "PUT" : "POST";

        const res = await fetch(url, {
            method: metodo,
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const data = await res.json();

        if (!res.ok) {
            alert(data.message || "Ocurrió un error.");
            return;
        }

        alert(data.message || "Operación realizada correctamente.");
        limpiarFormulario();
        await cargarReservaciones();

    } catch (err) {
        console.error("Error al guardar reservación:", err);
        alert("Error al guardar la reservación.");
    }
});

window.editarReservacion = function (id) {
    const r = reservaciones.find(x => x.id_reservacion === id);

    if (!r) {
        alert("No se encontró la reservación.");
        return;
    }

    editandoId = id;

    nombreInput.value = r.nombre_cliente || "";
    telefonoInput.value = r.telefono || "";
    fechaInput.value = r.fecha || "";
    horaInput.value = formatearHora(r.hora);
    personasInput.value = r.no_personas || "";
    estadoInput.value = r.estado || "Pendiente";
    notaInput.value = r.comentarios || "";
    actualizarHoraMinima();

    const submitBtn = form.querySelector("button[type='submit']");
    if (submitBtn) submitBtn.textContent = "Actualizar reservación";

    form.scrollIntoView({ behavior: "smooth", block: "start" });
};

window.eliminarReservacion = async function (id) {
    const confirmacion = confirm("¿Seguro que deseas eliminar esta reservación?");
    if (!confirmacion) return;

    try {
        const res = await fetch(`/api/reservaciones/${id}`, {
            method: "DELETE"
        });

        const data = await res.json();

        if (!res.ok) {
            alert(data.message || "No se pudo eliminar.");
            return;
        }

        alert(data.message || "Reservación eliminada correctamente.");
        await cargarReservaciones();

    } catch (err) {
        console.error("Error al eliminar reservación:", err);
        alert("No se pudo eliminar la reservación.");
    }
};

function exportarReservacionesPDF() {
    const tablaOriginal = document.querySelector(".table");
    if (!tablaOriginal) {
        alert("No se encontró la tabla de reservaciones para exportar.");
        return;
    }

    const tablaClon = tablaOriginal.cloneNode(true);

    tablaClon.querySelectorAll("tr").forEach(row => {
        if (row.cells.length > 0) {
            row.deleteCell(row.cells.length - 1);
        }
    });

    const ventana = window.open("", "_blank");
    if (!ventana) {
        alert("No se pudo abrir la ventana para generar el PDF. Revisa si el navegador bloqueó ventanas emergentes.");
        return;
    }

    ventana.document.write(`
        <html>
            <head>
                <title>Reservaciones</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        padding: 24px;
                    }

                    h2 {
                        text-align: center;
                        margin-bottom: 20px;
                    }

                    table {
                        width: 100%;
                        border-collapse: collapse;
                        font-size: 12px;
                    }

                    th, td {
                        border: 1px solid #ccc;
                        padding: 8px;
                        text-align: left;
                    }

                    th {
                        background: #f3f4f6;
                    }
                </style>
            </head>
            <body>
                <h2>Reporte de reservaciones</h2>
                ${tablaClon.outerHTML}
            </body>
        </html>
    `);

    ventana.document.close();

    setTimeout(() => {
        ventana.focus();
        ventana.print();
        ventana.close();
    }, 250);
}

btnLimpiar.addEventListener("click", limpiarFormulario);
searchByName.addEventListener("input", renderTabla);
telefonoInput.addEventListener("input", () => {
    telefonoInput.value = normalizarTelefono(telefonoInput.value);
});
fechaInput.addEventListener("change", actualizarHoraMinima);
horaInput.addEventListener("input", validarHoraInput);
horaInput.addEventListener("invalid", validarHoraInput);

if (btnExportarPDF) {
    btnExportarPDF.addEventListener("click", exportarReservacionesPDF);
}

btnBack.addEventListener("click", () => {
    const rol = localStorage.getItem("ROL");

    if (rol === "GERENTE") window.location.href = "/gerente";
    else if (rol === "HOSTESS") window.location.href = "/hostess";
    else if (rol === "JEFEDEPISO" || rol === "JEFEPISO") window.location.href = "/jefepiso";
    else window.location.href = "/";
});

fechaInput.setAttribute("min", obtenerFechaLocalHoy());
actualizarHoraMinima();

cargarReservaciones();
