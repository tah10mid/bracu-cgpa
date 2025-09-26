# 🚨 Streamlit Cloud Deployment Troubleshooting

## 🔧 Common Issues & Solutions

### 1. **Requirements Installation Errors**

If you see "Error installing requirements", try these solutions:

#### **Solution A: Use Alternative Requirements**
If PyMuPDF fails to install, rename files:
```bash
mv requirements.txt requirements_full.txt
mv requirements_minimal.txt requirements.txt
```

#### **Solution B: Remove System Packages**
If system packages cause issues, clear `packages.txt`:
```bash
echo "" > packages.txt
```

### 2. **PDF Parsing Not Available**

The app will work without PDF parsing! Users can:
- ✅ **Manual Entry**: Add courses manually
- ✅ **Full Analytics**: All CGPA tools still work
- ✅ **Planning Features**: Complete academic planning

### 3. **Import Errors**

If modules fail to import:
- Check all Python files are pushed to repository
- Verify `requirements.txt` has correct package names
- Ensure no circular imports

### 4. **Memory/Resource Issues**

If app crashes due to resources:
- Streamlit Cloud has limited resources
- PDF processing is memory-intensive
- Manual entry is more efficient

## 📋 Alternative Requirements Files

### **Full Version** (`requirements.txt`)
```
streamlit==1.28.1
plotly==5.17.0
pandas==2.1.4
numpy==1.25.2
PyMuPDF==1.23.14
```

### **Minimal Version** (`requirements_minimal.txt`)
```
streamlit==1.28.1
plotly==5.17.0
pandas==2.1.4
numpy==1.25.2
# PyMuPDF removed for compatibility
```

## 🎯 Deployment Strategy

1. **Try Full Version First**: With PDF parsing
2. **Fallback to Minimal**: If PyMuPDF fails
3. **Manual Entry Only**: Still fully functional!

## ⚡ Quick Fixes

### If App Won't Start:
```bash
# Use minimal requirements
git mv requirements.txt requirements_full.txt
git mv requirements_minimal.txt requirements.txt
git commit -m "Use minimal requirements for deployment"
git push
```

### If PDF Parsing Errors:
- App will show warning message
- Users can still use all other features
- Manual course entry works perfectly

## 🎓 App Features (Even Without PDF)

✅ **Manual Course Entry**
✅ **CGPA Calculation** 
✅ **Target CGPA Planning**
✅ **Analytics & Trends**
✅ **What-If Analysis**
✅ **Academic Planning**
✅ **Beautiful Visualizations**

**The app is fully functional even without PDF parsing!**

## 🚀 Success Indicators

When deployment works, you'll see:
- ✅ App loads without errors
- ✅ Manual course entry works
- ✅ Charts and analytics display
- ✅ CGPA calculations work
- ⚠️ PDF upload may show warning (that's OK!)

The CGPA projection tool is robust and works great even with minimal dependencies!