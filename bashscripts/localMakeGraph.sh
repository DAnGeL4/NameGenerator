echo "Start. Making Graph from dot file."
read -p "Profiling with tests (y/n)?" choice

case "$choice" in 
  "y" | "Y" ) 
  dot -Tpng -o logs/stats/profile/prof-graph-test.png logs/stats/graph/prof-data-test.dot
  ;;
  "n" | "N" ) 
  dot -Tpng -o logs/stats/profile/prof-graph.png logs/stats/graph/prof-data.dot
  ;;
  * ) 
  echo "invalid"
  ;;
esac

echo "Done."
