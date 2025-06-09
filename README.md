# 🤖 Bot Chuchu

Un bot automatizado de Twitter que comparte citas inspiradoras de poesía latinoamericana tres veces al día.

## 📖 Acerca del Bot

Bot Chuchu es un proyecto automatizado que rescata y difunde la riqueza literaria de los poetas latinoamericanos, compartiendo fragmentos selectos de sus obras para inspirar y conectar con la belleza de la palabra escrita.

### 🔗 Enlaces
- **Cuenta de Twitter/X:** [@Bot_Chuchu](https://x.com/Bot_Chuchu)

## ⏰ Horarios de Publicación

El bot publica automáticamente **3 veces al día** (hora de Panamá):
- 🌅 **10:00 AM** - 
- 🌆 **04:00 PM** - 
- 🌙 **08:00 PM** - 

## 🛠️ Tecnologías Utilizadas

- **Python 3.12** - Lenguaje principal
- **Tweepy** - API de Twitter/X
- **MongoDB** - Base de datos para almacenar citas
- **GitHub Actions** - Automatización y despliegue
- **python-dotenv** - Gestión de variables de entorno

## 📚 Características

- ✨ Selección curada de citas poéticas
- 🎯 Publicaciones automáticas programadas
- 📖 Información de fuente (libro y año)
- 🔄 Sistema de rotación para evitar repeticiones
- 📝 Registro de actividad (logs)

## 🚀 Funcionamiento

El bot utiliza GitHub Actions para ejecutarse automáticamente según el cronograma establecido:

1. Se conecta a la base de datos MongoDB
2. Selecciona una cita aleatoria no utilizada recientemente
3. Formatea el tweet con comillas y metadatos
4. Publica en Twitter/X
5. Registra la actividad en logs

## 📄 Formato de Tweets

```
"Cita del poeta..."

📖Libro: Nombre del Libro (Año)
```

## 🤝 Contribuciones

Este es un proyecto personal dedicado a la difusión de la literatura y principalmente la obra de Chuchu Martinez. Si tienes sugerencias de poetas o mejoras, no dudes en abrir un issue en github o mandar un DM.

## 📞 Contacto

Para consultas sobre el bot, puedes contactar a través de la cuenta [@Bot_Chuchu](https://x.com/Bot_Chuchu) o [@ericlucerog](https://x.com/ericlucerog).

---


## 📜 License  

MIT License  

```plaintext
Copyright (c) [Year] [Your Name/Organization]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.