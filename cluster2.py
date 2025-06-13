import streamlit as st
from redis.cluster import RedisCluster, ClusterNode
import matplotlib.pyplot as plt

st.set_page_config(page_title="Clés Redis Cluster", layout="centered")
st.title("🔗 Répartition des clés dans Redis Cluster")

# Connexion Redis Cluster
startup_nodes = [ClusterNode("127.0.0.1", 7001)]
rc = RedisCluster(startup_nodes=startup_nodes, decode_responses=True, skip_full_coverage_check=True)

# Saisie du nombre de clés à insérer
nb_cles = st.number_input("📥 Nombre de clés à insérer", min_value=1, max_value=1000, value=100, step=10)

if st.button("🚀 Insérer les clés dans le cluster"):
    for i in range(1, nb_cles + 1):
        key = f"user:{i}"
        value = f"User{i}"
        rc.set(key, value)
    st.success(f"✅ {nb_cles} clés insérées dans le cluster.")

# Calcul de la répartition
nodes_by_node = {}
for i in range(1, nb_cles + 1):
    key = f"user:{i}"
    try:
        node = rc.get_node_from_key(key)
        node_info = f"{node.host}:{node.port}"
        nodes_by_node.setdefault(node_info, []).append(key)
    except Exception as e:
        st.error(f"Erreur pour la clé {key} : {e}")

# Affichage de la répartition
if nodes_by_node:
    st.subheader("📊 Répartition des clés par nœud")
    for node, keys in nodes_by_node.items():
        st.write(f"🧠 Nœud `{node}` contient **{len(keys)}** clés.")

    # Graphique camembert
    labels = list(nodes_by_node.keys())
    sizes = [len(keys) for keys in nodes_by_node.values()]

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    ax.set_title("Répartition des clés par nœud Redis Cluster")
    ax.axis('equal')

    st.pyplot(fig)
else:
    st.info("ℹ️ Aucune clé trouvée. Cliquez sur le bouton pour insérer des clés.")
