/**
 * Bootstrap
 * (sails.config.bootstrap)
 *
 * An asynchronous bootstrap function that runs just before your Sails app gets lifted.
 * > Need more flexibility?  You can also do this by creating a hook.
 *
 * For more information on bootstrapping your app, check out:
 * https://sailsjs.com/config/bootstrap
 */

module.exports.bootstrap = async function(done) {

  // Import dependencies
  var path = require('path');

  // This bootstrap version indicates what version of fake data we're dealing with here.
  var HARD_CODED_DATA_VERSION = 0;

  // This path indicates where to store/look for the JSON file that tracks the "last run bootstrap info"
  // locally on this development computer (if we happen to be on a development computer).
  var bootstrapLastRunInfoPath = path.resolve(sails.config.appPath, '.tmp/bootstrap-version.json');

  // Whether or not to continue doing the stuff in this file (i.e. wiping and regenerating data)
  // depends on some factors:
  // - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

  // If the hard-coded data version has been incremented, or we're being forced
  // (i.e. `--drop` or `--environment=test` was set), then run the meat of this
  // bootstrap script to wipe all existing data and rebuild hard-coded data.
  if (sails.config.models.migrate !== 'drop' && sails.config.environment !== 'test') {
    // If this is _actually_ a production environment (real or simulated), or we have
    // `migrate: safe` enabled, then prevent accidentally removing all data!
    if (process.env.NODE_ENV==='production' || sails.config.models.migrate === 'safe') {
      sails.log.warn('Since we are running with migrate: \'safe\' and/or NODE_ENV=production (in the "'+sails.config.environment+'" Sails environment, to be precise), skipping the rest of the bootstrap to avoid data loss...');
      return done();
    }//•

    // Compare bootstrap version from code base to the version that was last run
    var lastRunBootstrapInfo = await sails.helpers.fs.readJson(bootstrapLastRunInfoPath)
    .tolerate('doesNotExist');// (it's ok if the file doesn't exist yet-- just keep going.)

    if (lastRunBootstrapInfo && lastRunBootstrapInfo.lastRunVersion === HARD_CODED_DATA_VERSION) {
      sails.log('Skipping v'+HARD_CODED_DATA_VERSION+' bootstrap script...  (because it\'s already been run)');
      sails.log('(last run on this computer: @ '+(new Date(lastRunBootstrapInfo.lastRunAt))+')');
      return done();
    }//•

    sails.log('Running v'+HARD_CODED_DATA_VERSION+' bootstrap script...  ('+(lastRunBootstrapInfo ? 'before this, the last time the bootstrap ran on this computer was for v'+lastRunBootstrapInfo.lastRunVersion+' @ '+(new Date(lastRunBootstrapInfo.lastRunAt)) : 'looks like this is the first time the bootstrap has run on this computer')+')');
  }
  else {
    sails.log('Running bootstrap script because it was forced...  (either `--drop` or `--environment=test` was used)');
  }

  // Since the hard-coded data version has been incremented, and we're running in
  // a "throwaway data" environment, delete all records from all models.
  for (let identity in sails.models) {
    await sails.models[identity].destroy({});
  }//∞

  // By convention, this is a good place to set up fake data during development.
  /*await User.createEach([
    { emailAddress: 'nsuat@unal.edu.co', fullName: 'Néstor Suat-Rojas', isSuperAdmin: true, password: await sails.helpers.passwords.hashPassword('1234') },
  ]);

  await Post.createEach([
    {id_source: 1234, created_at: '12/12/99', text: '@TransMilenio pésimo servicio alimentador ruta 11-5, 30 minutos esperando en el portal Suba y para colmo el conductor tratando mal a los pasajeros.. Que si no nos gustaba que cogieramos buseta! 😠😠Bus VDX213 ruta 11-5 4:40 pm'},
    {id_source: 5678, created_at: '12/12/99', text: "@angelamrobledo @petrogustavo ¿La marcha no era por la educación? Ah no, cierto que después era por el Iva. ¿Tampoco? ¿Ahora es para que le perdonen las multas a Petro ? Sean serios....Trabajen más bien en vez de seguir incendiado el país. #petroescaos"},
    {id_source: 9012, created_at: '12/12/99', text: "Mientras a mis compañeras de la of las recogió el amort, el amigo, el clandestino para salvarlas del beshoo trancon y manifestaciones a mí me recoge el sitp o en su defecto la rutica pirata 😩😩😩"},
    {id_source: 3456, created_at: '12/12/99', text: "Incidente vial entre 2 particulares 🚘 en la Autosur con Av. Villavicencio.Unidad de 👮 TransitoBta asignada."},
  ]);
*/

  // Save new bootstrap version
  await sails.helpers.fs.writeJson.with({
    destination: bootstrapLastRunInfoPath,
    json: {
      lastRunVersion: HARD_CODED_DATA_VERSION,
      lastRunAt: Date.now()
    },
    force: true
  })
  .tolerate((err)=>{
    sails.log.warn('For some reason, could not write bootstrap version .json file.  This could be a result of a problem with your configured paths, or, if you are in production, a limitation of your hosting provider related to `pwd`.  As a workaround, try updating app.js to explicitly pass in `appPath: __dirname` instead of relying on `chdir`.  Current sails.config.appPath: `'+sails.config.appPath+'`.  Full error details: '+err.stack+'\n\n(Proceeding anyway this time...)');
  });

  // Don't forget to trigger `done()` when this bootstrap function's logic is finished.
  // (otherwise your server will never lift, since it's waiting on the bootstrap)
  return done();

};
