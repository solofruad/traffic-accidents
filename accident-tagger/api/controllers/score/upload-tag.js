module.exports = {


  friendlyName: 'Upload tag',


  description: 'Este archivo procesa las peticiones que vienen del homepage con la clasificación del Tweet y lo guarda en la entidad Score',


  inputs: {
    id:{
      type: 'number',
      description: 'ID en la API del Tweet',
      required: true
    },
    label: {
      type: 'number',
      description: 'Clasificación elegida por el usuario',
      required: true
    },
    username:{
      type: 'string',
      description: 'Nombre de usuario quien registro la clasificación'
    }
  },


  exits: {
    success:{
      outputDescription: 'Information about the newly created record.',
      outputType:{
        id: 'number'
      }
    },
    badRequest: {
      description: 'La clasificación no pudo ser guardada',
      responseType: 'badRequest'
    }
  },


  fn: async function (inputs, exits) {
    if (inputs.id < 0){
      return exits.success({
        id: -1
      });
    }
    var isLogged = this.req.me ? 1 : 0;
    //Crear la clasificación
    var newScore = await Score.create({
      label: inputs.label,
      username: inputs.username,
      post: inputs.id,
      isLogged: isLogged
    }).fetch();

    //Revisar si ya se ha clasificado esta publicación m+as de 3 veces
    var count = await  Score.count({post: newScore.post});
    if (count > 2){
      //Si ya se clasificó más de 3 veces, cambiar registro 'complete' del modelo Post para que no se muestre más esta publicación
      await Post.updateOne({id:newScore.post}).set({complete:1});
    }
    return exits.success({
      id: newScore.id
    });

  }


};
