/**
 * Post.js
 *
 * @description :: A model definition.  Represents a database table/collection/etc.
 * @docs        :: https://sailsjs.com/docs/concepts/models-and-orm/models
 */

module.exports = {

  attributes: {

    //  ╔═╗╦═╗╦╔╦╗╦╔╦╗╦╦  ╦╔═╗╔═╗
    //  ╠═╝╠╦╝║║║║║ ║ ║╚╗╔╝║╣ ╚═╗
    //  ╩  ╩╚═╩╩ ╩╩ ╩ ╩ ╚╝ ╚═╝╚═╝
    id_source:{
      type: 'number',
      unique: true,
      example: 1234567890123,
      description: 'El identificador original de la publicacíón en la red social asociada.',
      required: true,
    },
    created_at:{
      type: 'string',
      example: '12/12/99',
      description: 'Fecha que fue creado la publicación en la red social.',
      required: true,
    },
    text:{
      type: 'string',
      description: 'Texto del mensaje o publicación de la red social.',
      required: true,
    },
    source:{
      type: 'string',
      description: 'La red social original de donde proviene la publicación',
      defaultsTo: 'twitter',
    },
    complete:{
      type: 'number',
      description: 'El post ya completó el máximo de clasificaciones echas por los usuarios',
      defaultsTo: 0,
    },

    //  ╔═╗╔╦╗╔╗ ╔═╗╔╦╗╔═╗
    //  ║╣ ║║║╠╩╗║╣  ║║╚═╗
    //  ╚═╝╩ ╩╚═╝╚═╝═╩╝╚═╝
    post_score:{
      collection: 'score',
      via: 'post'
    },

    //  ╔═╗╔═╗╔═╗╔═╗╔═╗╦╔═╗╔╦╗╦╔═╗╔╗╔╔═╗
    //  ╠═╣╚═╗╚═╗║ ║║  ║╠═╣ ║ ║║ ║║║║╚═╗
    //  ╩ ╩╚═╝╚═╝╚═╝╚═╝╩╩ ╩ ╩ ╩╚═╝╝╚╝╚═╝

  },

};

