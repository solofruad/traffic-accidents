# accident-tagger

Una aplicación para Etiquetar manualmente tweets en español


### Links

+ [Universidad Nacional de Colombia](https://unal.edu.co) 



### Version info

This app was originally generated on Thu May 23 2019 16:31:24 GMT-0500 (-05) using [Sails v1.0.2](https://sailsjs.com)

<!-- Internally, Sails used [`sails-generate@1.15.28`](https://github.com/balderdashy/sails-generate/tree/v1.15.28/lib/core-generators/new). -->



<!--
Note:  Generators are usually run using the globally-installed `sails` CLI (command-line interface).  This CLI version is _environment-specific_ rather than app-specific, thus over time, as a project's dependencies are upgraded or the project is worked on by different developers on different computers using different versions of Node.js, the Sails dependency in its package.json file may differ from the globally-installed Sails CLI release it was originally generated with.  (Be sure to always check out the relevant [upgrading guides](https://sailsjs.com/upgrading) before upgrading the version of Sails used by your app.  If you're stuck, [get help here](https://sailsjs.com/support).)
-->

### TODO
* Pulir cosas de interfaz link sueltos o algo parecido
* Hacer funcionar correo electronico y contacto para cualquier correo electronico (es decir, mailgun lo permita)
* Poner logo en correo electronico layout-email.ejs, cambiar nombre en asunto de correo
* Si la persona creo una cuenta, que no muestre tweets para etiquetar si el email no ha sido verificado
* Que este responsive
* Montar la base de datos
* Hacer deploy
 
### Comandos de interes
* sails generate page things/available-things
* sails console --redis
* sails generate model Thing
* sails console --redis
* sails generate action things/destroy-one-thing
* sails run scripts/rebuild-cloud-sdk.js 
* sails console --redis
* sails console --redis --drop
