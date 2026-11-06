const express = require("express");
const cors = require("cors");
const app = express();

const PORT = process.env.PORT || 3000;

// ✅ CORRECCIÓN SONARCLOUD: Restringir CORS a orígenes específicos
const allowedOrigins = [
  'http://localhost:5173', 
  'http://127.0.0.1:5173'
];

const corsOptions = {
  origin: function (origin, callback) {
    // Permitir peticiones sin origen (como aplicaciones móviles o Postman)
    if (!origin) return callback(null, true);
    
    // Si el origen está en la lista blanca, permitir
    if (allowedOrigins.indexOf(origin) !== -1) {
      callback(null, true);
    } else {
      callback(new Error('No permitido por CORS'));
    }
  },
  credentials: true // Permite el envío de cookies o headers de autorización
};

app.use(cors(corsOptions));

app.use(express.json());

// Ruta de prueba
app.get("/api/health", (req, res) => {
  res.json({ status: "OK", message: "Backend funcionando 🚀" });
});

app.listen(PORT, () => {
  console.log(`Servidor backend corriendo en http://localhost:${PORT}`);
});
