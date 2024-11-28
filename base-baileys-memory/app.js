const { postCompletion } = require('./chat'); 

const { createBot, createProvider, createFlow, addKeyword, EVENTS } = require('@builderbot/bot');

const { MemoryDB: Database } = require('@builderbot/bot');

const { BaileysProvider:provider } = require('@builderbot/provider-baileys')

const PORT = process.env.PORT ?? 3000

const mediaFlow  = addKeyword(EVENTS.MEDIA)
.addAnswer('Leyendo imagen....', { capture: false }, async (ctx, { provider }) => {
        const localPath = await provider.saveFile(ctx, {path:'./images'})
        ctx.localPath = localPath
})
.addAction(
    async (ctx, { flowDynamic }) => {
        const answer = await postCompletion(ctx.localPath);
        // Eliminar las comillas dobles al principio y al final de la cadena
        let cleanedAnswer = answer.replace(/^"(.*)"$/, '$1');

        // Decodificar caracteres escapados (si es necesario)
        cleanedAnswer = cleanedAnswer
            .replace(/\\n/g, '\n')  // Reemplazar saltos de línea escapados
            .replace(/\\u([\dA-F]{4})/gi, (match, group) => 
                String.fromCharCode(parseInt(group, 16))  // Decodificar unicode
            ).replace(/_/g, ' ');

        // Enviar texto decodificado a flowDynamic
        await flowDynamic(cleanedAnswer);
    }
)
   
    
const main = async () => {
    const adapterDB = new Database()
    const adapterFlow = createFlow([mediaFlow])
    const adapterProvider = createProvider(provider)

    const { httpServer }  = await createBot({
        flow: adapterFlow,
        provider: adapterProvider,
        database: adapterDB,
    })

    
    httpServer(+PORT)
    
}

main()

