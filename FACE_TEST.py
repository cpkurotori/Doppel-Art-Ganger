import cognitive_face as CF

KEY = '65fb1f6458eb4338a49b7c75e420eca2'  # Replace with a valid subscription key (keeping the quotes in place).
CF.Key.set(KEY)

# You can use this example JPG or replace the URL below with your own URL to a JPEG image.
img_url = 'https://www.biography.com/.image/c_fill%2Ccs_srgb%2Cg_face%2Ch_300%2Cq_80%2Cw_300/MTE1ODA0OTcxODExNDQwMTQx/vincent-van-gogh-9515695-3-402.jpg'
result = CF.face.detect(img_url)
print result
