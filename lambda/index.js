/*
 * Copyright 2019 Amazon.com, Inc. or its affiliates.  All Rights Reserved.
 *
 * You may not use this file except in compliance with the terms and conditions 
 * set forth in the accompanying LICENSE.TXT file.
 *
 * THESE MATERIALS ARE PROVIDED ON AN "AS IS" BASIS. AMAZON SPECIFICALLY DISCLAIMS, WITH 
 * RESPECT TO THESE MATERIALS, ALL WARRANTIES, EXPRESS, IMPLIED, OR STATUTORY, INCLUDING 
 * THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT.
*/

// This sample demonstrates sending directives to an Echo connected gadget from an Alexa skill
// using the Alexa Skills Kit SDK (v2). Please visit https://alexa.design/cookbook for additional
// examples on implementing slots, dialog management, session persistence, api calls, and more.

const Alexa = require('ask-sdk-core');
const Util = require('./util');
const Common = require('./common');

// The namespace of the custom directive to be sent by this skill
const NAMESPACE = 'Custom.Mindstorms.Gadget';

// The name of the custom directive to be sent this skill
const NAME_CONTROL = 'control';

const LaunchRequestHandler = {
    canHandle(handlerInput) {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'LaunchRequest';
    },
    handle: async function(handlerInput) {

        let request = handlerInput.requestEnvelope;
        let { apiEndpoint, apiAccessToken } = request.context.System;
        let apiResponse = await Util.getConnectedEndpoints(apiEndpoint, apiAccessToken);
        if ((apiResponse.endpoints || []).length === 0) {
            return handlerInput.responseBuilder
            .speak(`I couldn't find an EV3 Brick connected to this Echo device. Please check to make sure your EV3 Brick is connected, and try again.`)
            .getResponse();
        }

        // Store the gadget endpointId to be used in this skill session
        let endpointId = apiResponse.endpoints[0].endpointId || [];
        Util.putSessionAttribute(handlerInput, 'endpointId', endpointId);

        return handlerInput.responseBuilder
            .speak("Welcome, you can start issuing move commands")
            .reprompt("Awaiting commands")
            .getResponse();
    }
};


// Construct and send a custom directive to the connected gadget with data from
// the SetCommandIntent request.
const additionIntentHandler = {
    canHandle(handlerInput) {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'IntentRequest'
            && Alexa.getIntentName(handlerInput.requestEnvelope) === 'addition';
    },
    handle: function (handlerInput) {

        let command = 'adding'
        // if (!command) {
        //     return handlerInput.responseBuilder
        //         .speak("Can you repeat that?")
        //         .reprompt("What was that again?").getResponse();
        // }

        const attributesManager = handlerInput.attributesManager;
        let endpointId = attributesManager.getSessionAttributes().endpointId || [];
        // let speed = attributesManager.getSessionAttributes().speed || "50";
        let mState = attributesManager.getSessionAttributes().machinestate || "";

        // Construct the directive with the payload containing the move parameters
       
           const directive = Util.build(endpointId, NAMESPACE, NAME_CONTROL,
            {
                type: 'add',
                 numberone: "1",
                 numbertwo: "2"
            });
            
        return handlerInput.responseBuilder
            .speak(`Working on adding two numer`)
            .reprompt("awaiting command")
            .addDirective(directive)
            .getResponse();
    }
};

// The SkillBuilder acts as the entry point for your skill, routing all request and response
// payloads to the handlers above. Make sure any new handlers or interceptors you've
// defined are included below. The order matters - they're processed top to bottom.
exports.handler = Alexa.SkillBuilders.custom()
    .addRequestHandlers(
        LaunchRequestHandler,
        additionIntentHandler,
        // SetSpeedIntentHandler,
        // SetCommandIntentHandler,
        // MoveIntentHandler,
        Common.HelpIntentHandler,
        Common.CancelAndStopIntentHandler,
        Common.SessionEndedRequestHandler,
        Common.IntentReflectorHandler, // make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers
    )
    .addRequestInterceptors(Common.RequestInterceptor)
    .addErrorHandlers(
        Common.ErrorHandler,
    )
    .lambda();