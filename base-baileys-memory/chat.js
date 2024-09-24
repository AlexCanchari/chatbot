const { spawn } = require('child_process');
const fs = require('fs');

const postCompletion = async (filePath) => {
    return new Promise((resolve, reject) => {
        const python = spawn('python', ['./conexion_python.py']);
        
        let result = '';
        let error = '';

        python.stdout.on('data', (data) => {
            result += data.toString();
        });

        python.stderr.on('data', (data) => {
            error += data.toString();
        });

        python.on('close', (code) => {
            if (code !== 0) {
                reject(new Error(`Python script exited with code ${code}. Error: ${error}`));
            } else {
                resolve(result.trim());  
            }
        });

        // Enviar la ruta del archivo al script Python
        python.stdin.write(filePath);
        python.stdin.end();

    });
};

module.exports = { postCompletion };