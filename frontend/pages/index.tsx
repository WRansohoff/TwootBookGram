import React, {useState} from "react";
import Head from 'next/head';
import styles from '../styles/Home.module.css';
import DefaultLayout from "@/layouts/default";
import {Button, Card, CardBody, CardHeader, Modal, ModalContent, ModalHeader, ModalBody, ModalFooter, useDisclosure, Textarea} from "@nextui-org/react";

// Dictionary to track responses.
var responses = [
];

// Helper function to fetch responses from the AWS Lambda function.
export async function getResponses(setResponseLoading: any) {
  // Get the string to use as an initial social media post.
  let post = ''
  let postEl = document.getElementById("postEntry")
  // Make the linter happy by ensuring the element type is correct...
  if (postEl instanceof HTMLTextAreaElement) {
    post = postEl.value
  }

  // Debug: Log the submitted text.
  //console.log(post)

  // Disable the 'submit' button.
  setResponseLoading(true);

  // Fetch and process the responses.
  let response = await fetch('%%LAMBDA_FUNCTION_URL%%',
    {
      method: "POST",
      body: JSON.stringify({input: post})
    }).then(data => data.json())
      .then(resp => {
        responses = []
        // Process JSON response.
        // Debug: Log the structured response.
        //console.log(resp);

        // Render the responses on the page.
        let tweets = "";
        resp.responses.forEach((rjs) => {
          responses = responses.concat({'user': rjs['user'], 'response': rjs['response']});
        });

        // Debug: Log that the API call/post-process is complete.
        console.log('done');

        // Re-enable the 'submit' button.
        // TODO: If the user navigates away from the tab and the request
        // times out / never finishes, the button will be stuck in a
        // disabled state. Should catch that and print an explanation.
        setResponseLoading(false);
      })
}

// Main React component for the SPA.
export default function Home() {
  // React hook to let the app disable the 'submit' button while
  // responses are loading, and re-enable it afterwards.
  const [responseLoading, setResponseLoading] = useState(false);

  // Hooks for opening and closing the disclaimer modal.
  const {isOpen, onOpen, onOpenChange} = useDisclosure();

  // Core home page component.
  return (
    <>
      <DefaultLayout>
        <meta name="viewport" initial-scale={0} content="width=device-width" />
        <div className={styles.container}>
          <main>
            <h1 className={styles.title}>
              Welcome to TwootBookGram!
            </h1>
            <p className={styles.description}>
              <Button onClick={onOpen} color="secondary">
                Read this disclaimer before using the app.
              </Button>
            </p>
            <br/>
            <p className={styles.left_description}>
              Enter a short post into the text box below to view AI-generated responses.
              <div class={styles.line_spacer} />
              The language model is prompted to respond as a social media user.
              <div class={styles.line_spacer} />
              Most LLMs are trained on data that includes social media posts.
              <div class={styles.line_spacer} />
              In order to run this demo cheaply, I used a very small AI model, so the responses will not always make sense.
              <div class={styles.line_spacer} />
              The hardware is also cheap - serverless functions with 2GB RAM - so the responses take 1-2 minutes to generate.
            </p>
            <br/><br/>
            <div className={styles.description}>
              <Textarea
                 label="Post something"
                 placeholder="Enter your social media post"
                 className={styles.description}
                 id="postEntry"
                 maxLength={140}
              />
            </div>
            <div className={styles.description}>
              <Button color="primary" onClick={() => getResponses(setResponseLoading)} id="submitButton" isLoading={responseLoading}>
                Submit
              </Button>
            </div>
            <div className={styles.description}>
              <ul>
                {
                  responses.map((response) => {
                    let cols = ["#" + Math.floor(Math.random()*16777215).toString(16),
                                "#" + Math.floor(Math.random()*16777215).toString(16),
                                "#" + Math.floor(Math.random()*16777215).toString(16)];
                    let bg_col = {"background": "radial-gradient(circle at center, " + cols[0] + " 0, " + cols[1] + " 25%, " + cols[2] + " 100%)"};
                    let card_key = "response_" + response['user'];
                    return (
                      <Card key={card_key} className={styles.response_card}>
                        <CardHeader>
                          <span className={styles.response_icon} style={bg_col}>
                          </span>
                          <span className={styles.response_username}>
                            {response["user"]}
                          </span>
                        </CardHeader>
                        <CardBody>
                          <p className={styles.response_post}>
                            {response["response"]}
                          </p>
                        </CardBody>
                      </Card>
                    );
                  })
                }
              </ul>
            </div>
            <br/><br/>
            <footer>
            <div className={styles.description}>
              <a href="https://huggingface.co/facebook/opt-350m/blob/main/LICENSE.md" className={styles.linkStyle}>Source model: opt-350m</a>, quantized to 8-bit weights in OpenVINO format for CPU inference.
              <br/>
              Not for commercial use.
            </div>
            </footer>
          </main>
        </div>
      </DefaultLayout>

      <Modal isOpen={isOpen} onOpenChange={onOpenChange} size="md" scrollBehavior="inside">
        <ModalContent>
          {(onClose) => (
            <>
              <ModalHeader className="flex flex-col gap-1">Terms of Use Disclosure</ModalHeader>
              <ModalBody>
                <p>
                  This is a simple demonstration of how to serve a small AI language model using cheap serverless functions and model quantization. (AWS Lambda + OpenVINO in this case)
                </p>
                <p>
                  The model is prompted to generate short simulated social media posts in response to the message that you submit. The results that it generates are filtered to avoid a small set of highly inflammatory words, but this is not a product and it may generate offensive text.
                </p>
                <p>
                  <b>Use at your own risk</b>, and remember that the AI model has no understanding of concepts like "truth" or "reality". Everything that the model prints should be considered a work of fiction, and any relation to real people or events is entirely coincidental.
                </p>
              </ModalBody>
              <ModalFooter>
                <Button color="secondary" onClick={onClose}>Close</Button>
              </ModalFooter>
            </>
          )}
        </ModalContent>
      </Modal>
    </>
  );
}
