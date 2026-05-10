# apps/usuarios

**Propósito:** Extensión del perfil de usuario (teléfono, número de documento).

## Conexión de señales

`Perfil` se crea automáticamente mediante una señal `post_save` sobre `User`. La señal se registra en `UsuariosConfig.ready()` — si se mueve o renombra la configuración de la app, hay que volver a registrar la señal o `Perfil` no se creará para los nuevos usuarios.

No llamar a `Perfil.objects.create(user=...)` manualmente en las vistas — la señal lo gestiona.
