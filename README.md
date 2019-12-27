# EV3AlexaChallange
EV3 Alexa Challenge Hacker.io

## Essential code 

### mission - EV3 .py 

<code>       if command in ['add']:
          strSpeak = "Doing math, adding " + speed[0] + " and " + speed[1] + " is " + str(int(speed[0])+int(speed[1]))
          self.sound.speak(strSpeak)
          
        if command in ['primefactors']:
          factors = self.primeFactors(int(speed[0]) )
          primes  = Counter(factors)
          strMath = self.speakmath(primes)
          
          strSpeak = "Prime factors for " + speed[0] + " are " + strMath
          self.sound.speak(strSpeak)
</code>

## Essential code 

### index.js 

<code>
const additionIntentHandler = {
    canHandle(handlerInput) {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'IntentRequest'
            && Alexa.getIntentName(handlerInput.requestEnvelope) === 'addition';
    },
    handle: function (handlerInput) {

        // Bound speed to (1-100)
       
       // speed = Math.max(1, Math.min(100, parseInt(speed)));
      //    Util.putSessionAttribute(handlerInput, 'speed', speed);
      
       const attributesManager = handlerInput.attributesManager;

        const endpointId = attributesManager.getSessionAttributes().endpointId || [];
         let numberone = Alexa.getSlotValue(handlerInput.requestEnvelope, 'numberone');
        let numbertwo = Alexa.getSlotValue(handlerInput.requestEnvelope, 'numbertwo');

      const directive = Util.build(endpointId, NAMESPACE, NAME_CONTROL,
            {
                type: 'command',
                command: 'add',
                one: numberone,
                two: numbertwo
            });



        return handlerInput.responseBuilder
            .speak(`let me ask EV3`)
            .reprompt("what's next? multiply 2 numbers? ")
            .addDirective(directive)
            .getResponse();
    }
};

const primefactorsIntentHandler = {
    canHandle(handlerInput) {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'IntentRequest'
            && Alexa.getIntentName(handlerInput.requestEnvelope) === 'primefactors';
    },
    handle: function (handlerInput) {

        // Bound speed to (1-100)
       
       // speed = Math.max(1, Math.min(100, parseInt(speed)));
      //    Util.putSessionAttribute(handlerInput, 'speed', speed);
      
       const attributesManager = handlerInput.attributesManager;

        const endpointId = attributesManager.getSessionAttributes().endpointId || [];
        let numberone = Alexa.getSlotValue(handlerInput.requestEnvelope, 'numberone');
        let numbertwo = Alexa.getSlotValue(handlerInput.requestEnvelope, 'numberone');

      const directive = Util.build(endpointId, NAMESPACE, NAME_CONTROL,
            {
                type: 'command',
                command: 'primefactors',
                one: numberone,
                two: numbertwo
            });



        return handlerInput.responseBuilder
            .speak(`let me ask EV3`)
            .reprompt("what's next? add 33 and 22? ")
            .addDirective(directive)
            .getResponse();
    }
};

</code>
