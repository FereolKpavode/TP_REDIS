import streamlit as st
import redis

# Connexion Redis
r = redis.Redis(host='localhost', port=6379, db=0)
PANIER_TTL = 1800  # 30 minutes

st.set_page_config(page_title="Gestion de Panier Redis", layout="centered")
st.title("🛒 Interface de gestion de panier (Redis)")

# Saisie de l'utilisateur
user_id = st.text_input("🔑 Identifiant utilisateur", value="123")
cart_key = f"panier:user:{user_id}"

# Ajouter un article
st.subheader("➕ Ajouter un article")
article_id = st.text_input("ID de l'article")
quantite = st.number_input("Quantité", min_value=1, step=1)

if st.button("Ajouter au panier"):
    if article_id:
        r.hincrby(cart_key, article_id, int(quantite))
        r.expire(cart_key, PANIER_TTL)
        st.success(f"{quantite} x Article {article_id} ajouté.")
    else:
        st.warning("Veuillez entrer un ID d'article.")

# Afficher le panier
st.subheader("📦 Contenu du panier")
panier = r.hgetall(cart_key)
if panier:
    for k, v in panier.items():
        st.write(f"🧾 Article **{k.decode()}** — Quantité : **{int(v)}**")
else:
    st.info("Panier vide.")

# Supprimer un article
st.subheader("➖ Supprimer un article")
article_supp = st.text_input("ID de l'article à supprimer")
if st.button("Supprimer l'article"):
    if article_supp:
        r.hdel(cart_key, article_supp)
        st.success(f"Article {article_supp} supprimé.")
    else:
        st.warning("Veuillez entrer l'ID à supprimer.")

# Vider panier
if st.button("🗑️ Vider le panier"):
    r.delete(cart_key)
    st.success("Panier vidé.")

# TTL restant
st.subheader("⏳ Temps avant expiration du panier")
ttl = r.ttl(cart_key)
if ttl > 0:
    st.info(f"Temps restant : **{ttl}** secondes.")
elif ttl == -1:
    st.warning("Le panier n'expirera pas automatiquement.")
else:
    st.info("Aucun panier actif.")

