# TX Counter

A Cartes Dapp for counts transactions per sender then generates notices and reports for the data.

## Installation instructions

https://docs.cartesi.io/cartesi-rollups/1.3/development/installation/


## How to test

1. Clone the repo

2. Run ```cd txcount```

3. Run ```cartesi build```

4. Run ```cartesi run```

4. Run ```cartesi send``` on a new terminal tab and send a generic input to the application using foundry

5. Visit the graphql endpoint (http://localhost:8080/graphql) on your browser query notices
    ```
    query notices {
    notices {
        edges {
        node {
            index
            input {
            msgSender
            payload
            }
            payload
            proof {
            context
            }
        }
        }
    }
    }

    ```

6. Do an inspect request of the transactions count on your browser with the following url. 
http://localhost:8080/inspect/tx_counter
