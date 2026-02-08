uv pip install mkdocs mkdocs-material mkdocs-awesome-pages-plugin


uv run mkdocs serve &
servePID=$!


mkdir -p ./dist/docs
chmod 777 ./dist/docs


sleep 10

docker run \
--network host \
  -v ./dist/docs:/output \
  ghcr.io/openzim/zimit \
    zimit \
      --seeds http://localhost:8000/Zephyr \
      --name ZephyrDocs.zim \
      --title "Zephyr Documentation" \
      --creator "DeyanM1" \
      --publisher "DeyanM1" \
      --lang "en" \
      --description "Full documentation of the Zephyr programming Language by DeyanM1" \


kill $servePID
wait $servePID

rm -rf ./dist/docs/fails