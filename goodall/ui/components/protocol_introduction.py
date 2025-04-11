import streamlit as st


def render_protocol_introduction():
    st.subheader("Background")
    st.markdown("""
            Privacy-Preserving Record linkage (PPRL) is an essential component in <strong>data integration</strong> tasks of sensitive information. The linkage quality determines the usability of combined datasets and (machine learning) applications based on them.

            State-of-the-art record linkage solutions use supervised machine learning approaches that require labeled training data.
            Active learning methods aim to reduce the labeling effort by selecting informative samples for clerical review. However, they have not been applied in the PPRL domain yet.

            We present a novel privacy-preserving protocol that integrates clerical review in PPRL using a multi-layer <strong>active learning</strong> process.
            Uncertain match candidates are reviewed on several layers by human and non-human oracles to reduce the amount of disclosed information per record and in total.
            Predictions are propagated back to update previous layers, resulting in an improved linkage performance for non-reviewed candidates as well.
            The data owners remain in control of the amount of information they share for each record. Therefore, our approach follows need-to-know and data sovereignty principles.
            The experimental evaluation on real-world datasets shows considerable linkage quality improvements with limited labeling effort and privacy risks.
            """, unsafe_allow_html=True)
    with st.expander("Privacy-Preserving Record Linkage"):
        st.markdown("""
    <div width="100%" align="center">
    <img style="margin: 20px 0;" width="60%" src="app/static/images/record-linkage-motivation.png">
    </div>
    <div width="100%" align="center">
    <img style="margin: 20px 0;" width="50%" src="app/static/images/pprl-ttp-workflow.png">
    </div>
                """, unsafe_allow_html=True)
    with st.expander("Bloom filter encoding technique"):
        st.markdown("""
                Bloom filter encodings were proposed
    for PPRL by Schnell et al. They became the de-facto standard
    for practical PPRL on large datasets. The plaintext is tokenized
    and each token is mapped to multiple positions in the bit vector
    using cryptographic hash functions. Similar inputs lead to similar
    encodings which allows for fuzzy matching to tolerate typical data
    errors like typos. This transformation is not reversible due to collision
    where multiple features are hashed to the same position.
    <div width="100%" align="center">
    <img style="margin: 20px 0;" width="60%" src="app/static/images/bloom-filter-encoding.png">
    </div>
    Due to their similarity preserving transformation, Bloom filter encodings
    are susceptible to frequency attacks. Different encoding
    techniques to hamper such attacks have been proposed in the last
    years. Most importantly, multiple or all attributes are combined
    in a single encoded representation. Thereby, tokens from different
    attributes lead to colliding hashes. Attribute-level encodings that
    transform each attribute of a record separately should be avoided
    to prevent an alignment of frequent encoded attribute values to
    frequent plaintext values.
    <div width="100%" align="center">
    <img style="margin: 20px 0;" width="20%" src="app/static/images/frequency-alignment.png">
    </div>
                """, unsafe_allow_html=True)

    with st.expander("Multi-layer clerical review and active learning"):
        st.markdown("""
<div style="display: flex; justify-content: space-between; align-items: flex-start;">
  <div style="width: 45%; text-align: left;">
    <ul>
      <li><strong>Need-to-Know Principle:</strong> Multiple layers of classification to ensure minimal disclosure of information where data owners share only the necessary information for high-probability classification decisions.</li>
      <li><strong>Three-Layer Protocol:</strong>
        <ul>
          <li>Layer <code>L<sub>R</sub></code> uses record-level encodings (<code>E<sub>R</sub></code>) to automatically classify certain matches/non-matches with high level of privacy protection.</li>
          <li>Layer <code>L<sub>A</sub></code> automatically reviews uncertain pairs using keyed attribute-level encodings (<code>E<sub>A</sub></code>) for higher classification accuracy and to identify attributes needed for masked clerical review.</li>
          <li>Layer <code>L<sub>C</sub></code> manually resolves remaining uncertain pairs by masked clerical review using selected plaintext attributes.</li>
        </ul>
      </li>
      <li><strong>Active Learning:</strong> Two active learning processes: <code>𝒜𝐿<sub>R</sub></code> (trains <code>M<sub>R</sub></code> using <code>M<sub>A</sub></code> as an oracle) and <code>𝒜𝐿<sub>A</sub></code> (human oracle provides labels for <code>M<sub>A</sub></code>). Revised labels from lower layers update models in upper layers to improve classification accuracy iteratively.</li>
      <li><strong>Data Owner Participation:</strong> Data owners actively provide additional information through encodings but can limit disclosure for each record.</li>
    </ul>
  </div>
  <div style="width: 50%; text-align: center;">
    <img style="margin: 20px 0; width: 100%;" src="app/static/images/multi-layer-active-learning-workflow.png" alt="Multi-layer active learning workflow">
  </div>
</div>

                """, unsafe_allow_html=True)